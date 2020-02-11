#ifndef CARD_H_
#define CARD_H_

#include <string>

namespace card
{

struct Creature // 生物
{
    std::string name;    // 名字
    int available_count; // 生物槽容量
    int cost;            // 法力消耗
    int atk;             // 攻击
    int max_hp;          // 最大生命值
    int min_atk_range;   // 最小攻击范围
    int max_atk_range;   // 最大攻击范围
    int max_move;        // 行动力
    int cool_down;       // 冷却时间
    bool flying;         // 是否飞行
    bool atk_flying;     // 能否对空
    bool agility;        // 是否迅捷
    bool holy_shield;    // 有无圣盾
    Creature(std::string _name, int _count, int _cost, int _atk, int _maxhp,
             int _minatk, int _maxatk, int _maxmove, int _cool, bool _fly,
             bool _atkfly, bool _agility, bool _holyshield)
        : name(_name), available_count(_count), cost(_cost), atk(_atk),
          max_hp(_maxhp), min_atk_range(_minatk), max_atk_range(_maxatk),
          max_move(_maxmove), cool_down(_cool),
          flying(_fly), atk_flying(_atkfly),
          agility(_agility), holy_shield(_holyshield) {}
};

struct Artifact // 神器
{
    std::string name; // 名字
    int cost;         // 法力消耗
    int cool_down;    // 冷却时间
    Artifact(std::string _name, int _cost, int _cool)
        : name(_name), cost(_cost), cool_down(_cool) {}
};

// 剑士
const Creature SWORDMAN[4] = {Creature("Swordman", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                              Creature("Swordman", 4, 2, 2, 2, 1, 1, 3, 3, 0, 0, 0, 0),
                              Creature("Swordman", 4, 4, 4, 4, 1, 1, 3, 3, 0, 0, 0, 0),
                              Creature("Swordman", 4, 6, 6, 6, 1, 1, 3, 3, 0, 0, 0, 0)};

// 弓箭手
const Creature ARCHER[4] = {Creature("Archer", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            Creature("Archer", 3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0),
                            Creature("Archer", 3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0),
                            Creature("Archer", 3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0)};

// 黑蝙蝠
const Creature BLACKBAT[4] = {Creature("Archer", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                              Creature("Archer", 4, 2, 1, 1, 0, 1, 5, 2, 1, 1, 0, 0),
                              Creature("Archer", 4, 3, 2, 1, 0, 1, 5, 2, 1, 1, 0, 0),
                              Creature("Archer", 4, 5, 3, 2, 0, 1, 5, 2, 1, 1, 0, 0)};

// 牧师
const Creature PRIEST[4] = {Creature("Priest", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            Creature("Priest", 4, 2, 0, 2, 0, 0, 3, 4, 0, 0, 0, 0),
                            Creature("Priest", 4, 3, 0, 2, 0, 0, 3, 4, 0, 0, 0, 0),
                            Creature("Priest", 4, 5, 0, 3, 0, 0, 3, 5, 0, 0, 0, 0)};

// 火山之龙
const Creature VOLCANOGRAGON[4] = {Creature("VolcanoDragon", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                   Creature("VolcanoDragon", 3, 5, 3, 5, 1, 2, 3, 5, 0, 0, 0, 0),
                                   Creature("VolcanoDragon", 3, 7, 4, 7, 1, 2, 3, 5, 0, 0, 0, 0),
                                   Creature("VolcanoDragon", 3, 9, 5, 9, 1, 2, 3, 5, 0, 0, 0, 0)};

// 圣光之耀
const Artifact HOLYLIGHT = Artifact("HolyLight", 8, 6);
// 阳炎之盾
const Artifact SALAMANDERSHIELD = Artifact("SalamanderShield", 6, 6);
// 地狱之火
const Artifact INFERNOFLAME = Artifact("InfernoFlame", 6, 6);
// 地狱火
const Creature INFERNO = Creature("Inferno", 0, 0, 8, 8, 1, 1, 3, 0, 0, 0, 0, 0);

}; // namespace card

#endif