#include "ai_sdk.hpp"
#include "gameunit.hpp"
#include "calculator.h"
#include "card.h"

class AI
{
public:
    // 初始化卡牌
    AI(std::vector<std::string> artifacts, std::vector<std::string> creatures)
    {
        ai_sdk::init(artifacts, creatures);
    }

    // 更新游戏局面信息
    void updateGameInfo()
    {
        json game_info = ai_sdk::read();
        game_info["round"].get_to(round);
        game_info["camp"].get_to(my_camp);
        game_info["map"].get_to(map);
        game_info["players"][0].get_to(players[0]);
        game_info["players"][1].get_to(players[1]);
    }

    // 己方单位从位置pos_a到位置pos_b的地面距离(考虑被敌方地面生物阻挡但不考虑被敌方生物拦截)
    int getDistanceOnGround(gameunit::Pos pos_a, gameunit::Pos pos_b)
    {
        //地图边界
        std::vector<gameunit::Pos> obstacles_pos = calculator::MAPBORDER();
        //地面障碍
        for (auto p = map.ground_obstacles.begin(); p != map.ground_obstacles.end(); p++)
        {
            obstacles_pos.push_back(p->pos);
        }
        //敌方地面生物
        for (auto p = map.units.begin(); p != map.units.end(); p++)
        {
            if (p->camp != my_camp && (!p->flying))
            {
                obstacles_pos.push_back(p->pos);
            }
        }
        return calculator::search_path(pos_a, pos_b, obstacles_pos, {}).size();
    }

    // 己方单位从位置pos_a到位置pos_b的飞行距离(考虑被敌方飞行生物阻挡但不考虑被敌方生物拦截)
    int getDistanceInSky(gameunit::Pos pos_a, gameunit::Pos pos_b)
    {
        //地图边界
        std::vector<gameunit::Pos> obstacles_pos = calculator::MAPBORDER();
        //飞行障碍
        for (auto p = map.flying_obstacles.begin(); p != map.flying_obstacles.end(); p++)
        {
            obstacles_pos.push_back(p->pos);
        }
        //敌方飞行生物
        for (auto p = map.units.begin(); p != map.units.end(); p++)
        {
            if (p->camp != my_camp && p->flying)
            {
                obstacles_pos.push_back(p->pos);
            }
        }
        return calculator::search_path(pos_a, pos_b, obstacles_pos, {}).size();
    }

    // 对于指定位置pos,获取其上所有生物
    std::vector<gameunit::Unit> getUnits(gameunit::Pos pos)
    {
        std::vector<gameunit::Unit> units_on_pos;
        for (int i = 0; i < map.units.size(); ++i)
        {
            if (map.units[i].pos == pos)
                units_on_pos.push_back(map.units[i]);
        }
        return units_on_pos;
    }

    // 对于指定位置pos,判断其驻扎情况
    // 不是驻扎点返回-2,中立返回-1,否则返回占领该驻扎点的阵营(0/1)
    int checkBarrack(gameunit::Pos pos)
    {
        for (auto barrack = map.barracks.begin(); barrack != map.barracks.end(); barrack++)
        {
            if (barrack->pos == pos)
                return barrack->camp;
        }
        return -2;
    }

    // 判断生物attacker能否攻击到生物target(只考虑攻击力、攻击范围)
    bool canAttack(gameunit::Unit attacker, gameunit::Unit target)
    {
        //攻击力小于等于0的单位无法攻击
        if (attacker.atk <= 0)
            return false;
        //攻击范围
        int dist = calculator::cube_distance(attacker.pos, target.pos);
        if (dist < attacker.atk_range.first || dist > attacker.atk_range.second)
            return false;
        //对空攻击
        if (target.flying && (!attacker.atk_flying))
            return false;
        return true;
    }

    // 判断能否对位置pos使用神器artifact(不考虑消耗、冷却)
    bool canUseArtifact(gameunit::Artifact artifact, gameunit::Pos pos)
    {
        if (artifact.name == "HolyLight")
        {
            return calculator::in_map(pos);
        }
        else if (artifact.name == "InfernoFlame")
        {
            // 无地面生物
            for (auto unit = map.units.begin(); unit != map.units.end(); unit++)
            {
                if ((unit->pos == pos) && (not unit->flying))
                    return false;
            }
            // 距己方神迹范围<=5
            if (calculator::cube_distance(pos, map.relics[my_camp].pos) <= 5)
                return true;
            // 距己方占领驻扎点范围<=3
            for (auto barrack = map.barracks.begin(); barrack != map.barracks.end(); barrack++)
            {
                if ((barrack->camp == my_camp) && (calculator::cube_distance(pos, barrack->pos) <= 3))
                    return true;
            }
        }
        return false;
    }

    // 判断能否对生物pos使用神器artifact(不考虑消耗、冷却)
    bool canUseArtifact(gameunit::Artifact artifact, gameunit::Unit unit)
    {
        if (artifact.name == "SalamanderShield")
        {
            // 己方生物
            return artifact.camp == unit.camp;
        }
        return false;
    }

    void play()
    {
        if (round < 20)
            ai_sdk::endRound(round);
        else
            exit(0);
    }

private:
    int round;
    int my_camp;
    gameunit::Map map;
    gameunit::Player players[2];
};

int main()
{
    AI player_ai({"artifact"}, {"creature0", "creature1", "creature2"});
    while (true)
    {
        player_ai.updateGameInfo();
        player_ai.play();
    }
    return 0;
}
