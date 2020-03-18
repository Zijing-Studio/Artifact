#include "ai_client.h"
#include "gameunit.hpp"
#include "card.h"
#include "calculator.h"

using gameunit::Pos;
using card::CARD_DICT;

class AI : public AiClient
{
private:
    Pos miracle_pos;

    Pos enemy_pos;

    Pos target_barrack;

    Pos posShift(Pos pos, std::string direct);

public:
    //选择初始卡组
    void chooseCards(); //(根据初始阵营)选择初始卡组

    void play(); //玩家需要编写的ai操作函数

    void battle();

    void march();
};

void AI::chooseCards()
{
    // (根据初始阵营)选择初始卡组

    /*
     * artifacts和creatures可以修改
     * 【进阶】在选择卡牌时，就已经知道了自己的所在阵营和先后手，因此可以在此处根据先后手的不同设置不同的卡组和神器
     */
    my_artifacts = {"HolyLight"};
    my_creatures = {"Archer", "Swordsman", "VolcanoDragon"};
    init();
}

void AI::play()
{
    //玩家需要编写的ai操作函数

    /*
    本AI采用这样的策略：
    在首回合进行初期设置、在神迹优势路侧前方的出兵点召唤一个1星弓箭手
    接下来的每回合，首先尽可能使用神器，接着执行生物的战斗，然后对于没有进行战斗的生物，执行移动，最后进行召唤
    在费用较低时尽可能召唤星级为1的兵，优先度剑士>弓箭手>火山龙
    【进阶】可以对局面进行评估，优化神器的使用时机、调整每个生物行动的顺序、调整召唤的位置和生物种类、星级等
    */
    if (round == 0 || round == 1) {
        //先确定自己的基地、对方的基地
        miracle_pos = map.miracles[my_camp].pos;
        enemy_pos = map.miracles[my_camp ^ 1].pos;
        //设定目标驻扎点为最近的驻扎点

        target_barrack = map.barracks[0].pos;
        //确定离自己基地最近的驻扎点的位置
        for (auto barrack:map.barracks) {
            if (calculator::cube_distance(miracle_pos, barrack.pos) <
                calculator::cube_distance(miracle_pos, target_barrack))
                target_barrack = barrack.pos;
        }

        // 在正中心偏右召唤一个弓箭手，用来抢占驻扎点
        summon("Archer", 1, posShift(miracle_pos, "SF"));
    } else {
        //神器能用就用，选择覆盖单位数最多的地点
        if (players[my_camp].mana >= 6 && players[my_camp].artifact[0].state == "Ready") {
            auto pos_list = calculator::all_pos_in_map();
            auto best_pos = pos_list[0];
            int max_benefit = 0;
            for (auto pos:pos_list) {
                auto unit_list = calculator::units_in_range(pos, 2, map, my_camp);
                if (unit_list.size() > max_benefit) {
                    best_pos = pos;
                    max_benefit = unit_list.size();
                }
            }
            use(players[my_camp].artifact[0].id, best_pos);
        }

        //之后先战斗，再移动
        battle();

        march();

        //最后进行召唤
        //将所有本方出兵点按照到对方基地的距离排序，从近到远出兵
        auto summon_pos_list = getSummonPosByCamp(my_camp);
        sort(summon_pos_list.begin(), summon_pos_list.end(), [this](Pos _pos1, Pos _pos2) {
            return calculator::cube_distance(_pos1, enemy_pos) < calculator::cube_distance(_pos2, enemy_pos);
        });
        std::vector<Pos> available_summon_pos_list;
        for (auto pos:summon_pos_list) {
            auto unit_on_pos_ground = getUnitsByPos(pos, false);
            if (unit_on_pos_ground.id == -1) available_summon_pos_list.push_back(pos);
        }

        //统计各个生物的可用数量，在假设出兵点无限的情况下，按照1个剑士、1个弓箭手、1个火山龙的顺序召唤
        int mana = players[my_camp].mana;
        auto deck = players[my_camp].creature_capacity;
        std::map<std::string, int> available_count;
        for (auto card_unit:deck)
            available_count[card_unit.type] = card_unit.available_count;

        std::vector<std::string> summon_list;
        //剑士和弓箭手数量不足或者格子不足则召唤火山龙
        if ((available_summon_pos_list.size() == 1 || available_count["Swordsman"] + available_count["Archer"] < 2) &&
            mana >= CARD_DICT.at("VolcanoDragon")[1].cost && available_count["VolcanoDragon"] > 0) {
            summon_list.push_back("VolcanoDragon");
            mana -= CARD_DICT.at("VolcanoDragon")[1].cost;
        }

        bool suc = true;
        while (mana >= 2 && suc) {
            suc = false;
            if (available_count["Swordsman"] > 0 && mana >= CARD_DICT.at("Swordsman")[1].cost) {
                summon_list.push_back("Swordsman");
                mana -= CARD_DICT.at("Swordsman")[1].cost;
                available_count["Swordsman"] -= 1;
                suc = true;
            }
            if (available_count["Archer"] > 0 && mana >= CARD_DICT.at("Archer")[1].cost) {
                summon_list.push_back("Archer");
                mana -= CARD_DICT.at("Archer")[1].cost;
                available_count["Archer"] -= 1;
                suc = true;
            }
            if (available_count["VolcanoDragon"] > 0 && mana >= CARD_DICT.at("VolcanoDragon")[1].cost) {
                summon_list.push_back("VolcanoDragon");
                mana -= CARD_DICT.at("VolcanoDragon")[1].cost;
                available_count["VolcanoDragon"] -= 1;
                suc = true;
            }
        }

        int i = 0;
        for (auto pos:available_summon_pos_list) {
            if (i == summon_list.size()) break;
            summon(summon_list[i], 1, pos);
            ++i;
        }
        endRound();
    }
}

Pos AI::posShift(Pos pos, std::string direct)
{
    /*
     * 对于给定位置，给出按照自己的视角（神迹在最下方）的某个方向移动一步后的位置
     * 本段代码可以自由取用
     * @param pos:  (x, y, z)
     * @param direct: 一个str，含2个字符，意义见注释
     * @return: 移动后的位置 (x', y', z')
     */
    transform(direct.begin(), direct.end(), direct.begin(), ::toupper);
    if (my_camp == 0) {
        if (direct == "FF")  //正前方
            return Pos(std::get<0>(pos) + 1, std::get<1>(pos) - 1, std::get<2>(pos));
        else if (direct == "SF")  //优势路前方（自身视角右侧为优势路）
            return Pos(std::get<0>(pos) + 1, std::get<1>(pos), std::get<2>(pos) - 1);
        else if (direct == "IF")  //劣势路前方
            return Pos(std::get<0>(pos), std::get<1>(pos) + 1, std::get<2>(pos) - 1);
        else if (direct == "BB")  //正后方
            return Pos(std::get<0>(pos) - 1, std::get<1>(pos) + 1, std::get<2>(pos));
        else if (direct == "SB")  //优势路后方
            return Pos(std::get<0>(pos), std::get<1>(pos) - 1, std::get<2>(pos) + 1);
        else if (direct == "IB")  //劣势路后方
            return Pos(std::get<0>(pos) - 1, std::get<1>(pos), std::get<2>(pos) + 1);
    } else {
        if (direct == "FF")  //正前方
            return Pos(std::get<0>(pos) - 1, std::get<1>(pos) + 1, std::get<2>(pos));
        else if (direct == "SF")  //优势路前方（自身视角右侧为优势路）
            return Pos(std::get<0>(pos) - 1, std::get<1>(pos), std::get<2>(pos) + 1);
        else if (direct == "IF")  //劣势路前方
            return Pos(std::get<0>(pos), std::get<1>(pos) - 1, std::get<2>(pos) + 1);
        else if (direct == "BB")  //正后方
            return Pos(std::get<0>(pos) + 1, std::get<1>(pos) - 1, std::get<2>(pos));
        else if (direct == "SB")  //优势路后方
            return Pos(std::get<0>(pos), std::get<1>(pos) + 1, std::get<2>(pos) - 1);
        else if (direct == "IB")  //劣势路后方
            return Pos(std::get<0>(pos) + 1, std::get<1>(pos), std::get<2>(pos) - 1);
    }
}

void AI::battle()
{

}

void AI::march()
{

}

int main()
{
    AI player_ai;
    player_ai.chooseCards();
    while (true) {
        player_ai.updateGameInfo();
        player_ai.play();
    }
    return 0;
}
