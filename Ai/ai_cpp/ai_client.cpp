#include "ai_client.h"
#include "calculator.h"

void AiClient::updateGameInfo()
{
    json game_info = read();
    game_info["round"].get_to(round);
    game_info["camp"].get_to(my_camp);
    game_info["map"].get_to(map);
    game_info["players"][0].get_to(players[0]);
    game_info["players"][1].get_to(players[1]);
}

void AiClient::chooseCards()
{
    my_artifacts = {"HolyLight"};
    my_creatures = {"Archer", "Swordman", "Priest"};
    init();
}

void AiClient::init()
{
    json operation_parameters;
    operation_parameters["artifacts"] = my_artifacts;
    operation_parameters["creatures"] = my_creatures;
    sendMsg(my_camp, 0, "init", operation_parameters);
}

void AiClient::summon(int type, int star, int x, int y, int z)
{
    json operation_parameters;
    std::vector<int> position = {x, y, z};
    operation_parameters["position"] = position;
    operation_parameters["type"] = type;
    operation_parameters["star"] = star;
    sendMsg(my_camp, round, "summon", operation_parameters);
}

void AiClient::summon(int type, int star, std::vector<int> position)
{
    json operation_parameters;
    operation_parameters["position"] = position;
    operation_parameters["type"] = type;
    operation_parameters["star"] = star;
    sendMsg(my_camp, round, "summon", operation_parameters);
}

void AiClient::summon(int type, int star, std::tuple<int, int, int> position)
{
    json operation_parameters;
    operation_parameters["position"] = position;
    operation_parameters["type"] = type;
    operation_parameters["star"] = star;
    sendMsg(my_camp, round, "summon", operation_parameters);
}

void AiClient::move(int mover, int x, int y, int z)
{
    json operation_parameters;
    operation_parameters["mover"] = mover;
    std::vector<int> position = {x, y, z};
    operation_parameters["position"] = position;
    sendMsg(my_camp, round, "move", operation_parameters);
}

void AiClient::move(int mover, std::vector<int> position)
{
    json operation_parameters;
    operation_parameters["mover"] = mover;
    operation_parameters["position"] = position;
    sendMsg(my_camp, round, "move", operation_parameters);
}

void AiClient::move(int mover, std::tuple<int, int, int> position)
{
    json operation_parameters;
    operation_parameters["mover"] = mover;
    operation_parameters["position"] = position;
    sendMsg(my_camp, round, "move", operation_parameters);
}

void AiClient::attack(int attacker, int target)
{
    json operation_parameters;
    operation_parameters["attacker"] = attacker;
    operation_parameters["target"] = target;
    sendMsg(my_camp, round, "attack", operation_parameters);
}

void AiClient::use(int artifact, int target)
{
    json operation_parameters;
    operation_parameters["card"] = artifact;
    operation_parameters["target"] = target;
    sendMsg(my_camp, round, "attack", operation_parameters);
}

void AiClient::use(int artifact, std::vector<int> target)
{
    json operation_parameters;
    operation_parameters["card"] = artifact;
    operation_parameters["target"] = target;
    sendMsg(my_camp, round, "attack", operation_parameters);
}

void AiClient::use(int artifact, std::tuple<int, int, int> target)
{
    json operation_parameters;
    operation_parameters["card"] = artifact;
    operation_parameters["target"] = target;
    sendMsg(my_camp, round, "attack", operation_parameters);
}

void AiClient::endRound()
{
    json operation_parameters;
    sendMsg(my_camp, round, "endround", operation_parameters);
}


int AiClient::getDistanceOnGround(gameunit::Pos pos_a, gameunit::Pos pos_b, int camp)
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
        if (p->camp != camp && (!p->flying))
        {
            obstacles_pos.push_back(p->pos);
        }
    }
    return calculator::search_path(pos_a, pos_b, obstacles_pos, {}).size();
}

int AiClient::getDistanceInSky(gameunit::Pos pos_a, gameunit::Pos pos_b, int camp)
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
        if (p->camp != camp && p->flying)
        {
            obstacles_pos.push_back(p->pos);
        }
    }
    return calculator::search_path(pos_a, pos_b, obstacles_pos, {}).size();
}

int AiClient::checkBarrack(gameunit::Pos pos)
{
    for (auto barrack = map.barracks.begin(); barrack != map.barracks.end(); barrack++)
    {
        if (barrack->pos == pos)
            return barrack->camp;
    }
    return -2;
}

bool AiClient::canAttack(gameunit::Unit attacker, gameunit::Unit target)
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

bool AiClient::canUseArtifact(gameunit::Artifact artifact, gameunit::Pos pos, int camp)
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
        if (calculator::cube_distance(pos, map.relics[camp].pos) <= 5)
            return true;
        // 距己方占领驻扎点范围<=3
        for (auto barrack = map.barracks.begin(); barrack != map.barracks.end(); barrack++)
        {
            if ((barrack->camp == camp) && (calculator::cube_distance(pos, barrack->pos) <= 3))
                return true;
        }
    }
    return false;
}

bool AiClient::canUseArtifact(gameunit::Artifact artifact, gameunit::Unit unit)
{
    if (artifact.name == "SalamanderShield")
    {
        // 己方生物
        return artifact.camp == unit.camp;
    }
    return false;
}

gameunit::Unit AiClient::getUnitsByPos(gameunit::Pos pos, bool flying)
{
    for (int i = 0; i < map.units.size(); ++i)
    {
        if (map.units[i].pos == pos && map.units[i].flying == flying)
            return map.units[i];
    }
    // 未找到时返回一个id为-1的Unit
    gameunit::Unit no_unit;
    no_unit.id = -1;
    return no_unit;
}

gameunit::Unit AiClient::getUnitById(int unit_id)
{
    for (int i = 0; i < map.units.size(); ++i)
    {
        if (map.units[i].id == unit_id)
            return map.units[i];
    }
    // 未找到时返回一个id为-1的Unit
    gameunit::Unit no_unit;
    no_unit.id = -1;
    return no_unit;
}

std::vector<gameunit::Unit> AiClient::getUnitsByCamp(int unit_camp)
{
    std::vector<gameunit::Unit> camp_units;
    for (int i = 0; i < map.units.size(); ++i)
    {
        if (map.units[i].camp == unit_camp)
            camp_units.push_back(map.units[i]);
    }
    return camp_units;
}

std::vector<gameunit::Pos> AiClient::getSummonPosByCamp(int camp)
{
    std::vector<gameunit::Pos> summon_pos;
    for (auto relic = map.relics.begin(); relic != map.relics.end(); relic++)
    {
        if (relic->camp == camp)
            summon_pos.insert(summon_pos.end(), relic->summon_pos_list.begin(), relic->summon_pos_list.end());
    }
    for (auto barrack = map.barracks.begin(); barrack != map.barracks.end(); barrack++)
    {
        if (barrack->camp == camp)
            summon_pos.insert(summon_pos.end(), barrack->summon_pos_list.begin(), barrack->summon_pos_list.end());
    }
    return summon_pos;
}
