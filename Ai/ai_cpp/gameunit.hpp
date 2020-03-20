#ifndef GAMEUNIT_HPP_
#define GAMEUNIT_HPP_

#include <vector>
#include <string>
#include <tuple>
#include "json.hpp"
using json = nlohmann::json;

namespace gameunit
{

typedef std::tuple<int, int, int> Pos; // 坐标

struct Unit // 生物
{
    int id;                     // id
    int camp;                   // 阵营
    std::string type;           // 种类
    int cost;                   // 法力消耗
    int atk;                    // 攻击
    int max_hp;                 // 生命上限
    int hp;                     // 当前生命
    std::vector<int> atk_range; // 最小攻击范围 最大攻击范围
    int max_move;               // 行动力
    int cool_down;              // 冷却时间
    Pos pos;                    // 位置
    int level;                  // 等级
    bool flying;                // 是否飞行
    bool atk_flying;            // 是否对空
    bool agility;               // 是否迅捷
    bool holy_shield;           // 有无圣盾
    bool can_atk;               // 能否攻击
    bool can_move;              // 能否移动
};

struct Barrack // 驻扎点
{
    Pos pos;                          // 位置
    int camp;                         // 阵营
    std::vector<Pos> summon_pos_list; // 出兵点位置
    Barrack(int _camp, Pos _pos, std::vector<Pos> _list) : pos(_pos), camp(_camp), summon_pos_list(_list) {}
};

struct Miracle // 神迹
{
    int camp;                         // 阵营
    int max_hp;                       // 最大生命值
    int hp;                           // 当前生命值
    Pos pos;                          // 位置
    std::vector<Pos> summon_pos_list; // 初始出兵点位置
    int id;                           // id
    Miracle(int _camp, int _maxhp, int _hp, Pos _pos, std::vector<Pos> _list, int _id) : camp(_camp), max_hp(_maxhp), hp(_hp), pos(_pos), summon_pos_list(_list), id(_id) {}
};

struct Obstacle
{
    std::string type;  // 种类
    Pos pos;           // 位置
    bool allow_flying; // 是否允许飞行生物通过
    bool allow_ground; // 是否允许地面生物通过
    Obstacle(std::string _type, Pos _pos, bool _f, bool _g) : type(_type), pos(_pos), allow_flying(_f), allow_ground(_g) {}
};

struct Artifact // 神器
{
    int id;                  // id
    std::string name;        // 名字
    int camp;                // 阵营
    int cost;                // 法力消耗
    int max_cool_down;       // 最大冷却时间
    int cool_down_time;      // 当前冷却时间
    std::string state;       // 使用状态
    std::string target_type; // 目标种类
};

struct CreatureCapacity
{
    std::string type;                // 种类
    int available_count;             // 生物槽容量
    std::vector<int> cool_down_list; // 冷却时间
};

struct Map // 地图
{
    std::vector<Unit> units;
    std::vector<Barrack> barracks;
    std::vector<Miracle> miracles;
    std::vector<Obstacle> obstacles;
    std::vector<Obstacle> flying_obstacles;
    std::vector<Obstacle> ground_obstacles;
    Map()
    {
        barracks = {Barrack(-1, {-6, -6, 12}, {{-7, -5, 12}, {-5, -7, 12}, {-5, -6, 11}}),
                    Barrack(-1, {6, 6, -12}, {{7, 5, -12}, {5, 7, -12}, {5, 6, -11}}),
                    Barrack(-1, {0, -5, 5}, {{0, -4, 4}, {-1, -4, 5}, {-1, -5, 6}}),
                    Barrack(-1, {0, 5, -5}, {{0, 4, -4}, {1, 4, -5}, {1, 5, -6}})};
        miracles = {Miracle(0, 30, 30, {-7, 7, 0}, {{-8, 6, 2}, {-7, 6, 1}, {-6, 6, 0}, {-6, 7, -1}, {-6, 8, -2}}, 0),
                    Miracle(1, 30, 30, {7, -7, 0}, {{8, -6, -2}, {7, -6, -1}, {6, -6, 0}, {6, -7, 1}, {6, -8, 2}}, 1)};
        obstacles = {Obstacle("Miracle", {-7, 7, 0}, false, false),
                     Obstacle("Miracle", {7, -7, 0}, false, false)};
        std::vector<Pos> ABYSS_POS_LIST = {{0, 0, 0}, {-1, 0, 1}, {0, -1, 1}, {1, -1, 0}, {1, 0, -1}, {0, 1, -1}, {-1, 1, 0}, {-2, -1, 3}, {-1, -2, 3}, {-2, -2, 4}, {-3, -2, 5}, {-4, -4, 8}, {-5, -4, 9}, {-4, -5, 9}, {-5, -5, 10}, {-6, -5, 11}, {1, 2, -3}, {2, 1, -3}, {2, 2, -4}, {3, 2, -5}, {4, 4, -8}, {5, 4, -9}, {4, 5, -9}, {5, 5, -10}, {6, 5, -11}};
        for (int i = 0; i < ABYSS_POS_LIST.size(); ++i)
            obstacles.push_back(Obstacle("Abyss", ABYSS_POS_LIST[i], true, false));
        ground_obstacles = obstacles;
    }
};

struct Player // 玩家
{
    int camp;                       // 阵营
    std::vector<Artifact> artifact; // 神器
    int mana;                       // 当前法力值
    int max_mana;                   // 最大法力值
    std::vector<CreatureCapacity> creature_capacity;
    std::vector<int> new_summoned_id_list; // 最新召唤的生物id
};

void from_json(const json &j, Unit &u)
{
    j[0].get_to(u.id);
    j[1].get_to(u.camp);
    j[2].get_to(u.type);
    j[3].get_to(u.cost);
    j[4].get_to(u.atk);
    j[5].get_to(u.max_hp);
    j[6].get_to(u.hp);
    j[7].get_to(u.atk_range);
    j[8].get_to(u.max_move);
    j[9].get_to(u.cool_down);
    j[10].get_to(u.pos);
    j[11].get_to(u.level);
    j[12].get_to(u.flying);
    j[13].get_to(u.atk_flying);
    j[14].get_to(u.agility);
    j[15].get_to(u.holy_shield);
    j[16].get_to(u.can_atk);
    j[17].get_to(u.can_move);
}

void from_json(const json &j, Artifact &a)
{
    j[0].get_to(a.camp);
    j[1].get_to(a.name);
    a.id = a.camp;
    j[2].get_to(a.cost);
    j[3].get_to(a.max_cool_down);
    j[4].get_to(a.cool_down_time);
    j[5].get_to(a.state);
    j[6].get_to(a.target_type);
}

void from_json(const json &j, CreatureCapacity &c)
{
    j[0].get_to(c.type);
    j[1].get_to(c.available_count);
    j[2].get_to(c.cool_down_list);
}

void from_json(const json &j, Map &m)
{
    j.at("units").get_to(m.units);
    json barracks_camp = j["barracks"];
    for (int i = 0; i < barracks_camp.size(); ++i)
        m.barracks[i].camp = barracks_camp[i];
    json miracle_hp = j["miracles"];
    m.miracles[0].hp = miracle_hp[0];
    m.miracles[1].hp = miracle_hp[1];
}

void from_json(const json &j, Player &p)
{
    j[0].get_to(p.artifact);
    j[1].get_to(p.mana);
    j[2].get_to(p.max_mana);
    j[3].get_to(p.creature_capacity);
    j[4].get_to(p.new_summoned_id_list);
}

} // namespace gameunit

#endif