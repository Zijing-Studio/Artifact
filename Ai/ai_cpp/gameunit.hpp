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
    int id;                        // id
    int camp;                      // 阵营
    std::string type;              // 种类
    std::string name;              // 名字
    int cost;                      // 法力消耗
    int atk;                       // 攻击
    int max_hp;                    // 生命上限
    int hp;                        // 当前生命
    std::pair<int, int> atk_range; // 最小攻击范围 最大攻击范围
    int max_move;                  // 行动力
    int cool_down;                 // 冷却时间
    Pos pos;                       // 位置
    int level;                     // 等级
    bool flying;                   // 是否飞行
    bool atk_flying;               // 是否对空
    bool agility;                  // 是否迅捷
    bool holy_shield;              // 有无圣盾
    bool can_atk;                  // 能否攻击
    bool can_move;                 // 能否移动
};

struct Barrack // 驻扎点
{
    Pos pos;                          // 位置
    int camp;                         // 阵营
    std::vector<Pos> summon_pos_list; // 出兵点位置
};

struct Relic // 神迹
{
    int camp;                         // 阵营
    int max_hp;                       // 最大生命值
    int hp;                           // 当前生命值
    Pos pos;                          // 位置
    std::vector<Pos> summon_pos_list; // 初始出兵点位置
    std::string name;                 // 名字
    int id;                           // id
};

struct Obstacle
{
    std::string type;  // 种类
    Pos pos;           // 位置
    bool allow_flying; // 是否允许飞行单位通过
    bool allow_ground; // 是否允许地面单位通过
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
    std::vector<Relic> relics;
    std::vector<Obstacle> obstacles;
    std::vector<Obstacle> flying_obstacles;
    std::vector<Obstacle> ground_obstacles;
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
    j.at("id").get_to(u.id);
    j.at("camp").get_to(u.camp);
    j.at("type").get_to(u.type);
    j.at("name").get_to(u.name);
    j.at("cost").get_to(u.cost);
    j.at("atk").get_to(u.atk);
    j.at("max_hp").get_to(u.max_hp);
    j.at("hp").get_to(u.hp);
    j.at("atk_range").get_to(u.atk_range);
    j.at("max_move").get_to(u.max_move);
    j.at("cool_down").get_to(u.cool_down);
    j.at("pos").get_to(u.pos);
    j.at("level").get_to(u.level);
    j.at("flying").get_to(u.flying);
    j.at("atk_flying").get_to(u.atk_flying);
    j.at("agility").get_to(u.agility);
    j.at("holy_shield").get_to(u.holy_shield);
    j.at("can_atk").get_to(u.can_atk);
    j.at("can_move").get_to(u.can_move);
}

void from_json(const json &j, Barrack &b)
{
    j.at("pos").get_to(b.pos);
    if (j["camp"].is_null())
        b.camp = -1;
    else
        j.at("camp").get_to(b.camp);
    j.at("summon_pos_list").get_to(b.summon_pos_list);
}

void from_json(const json &j, Relic &r)
{
    j.at("camp").get_to(r.camp);
    j.at("max_hp").get_to(r.max_hp);
    j.at("hp").get_to(r.hp);
    j.at("pos").get_to(r.pos);
    j.at("summon_pos_list").get_to(r.summon_pos_list);
    j.at("name").get_to(r.name);
    j.at("id").get_to(r.id);
}

void from_json(const json &j, Obstacle &o)
{
    j.at("type").get_to(o.type);
    j.at("pos").get_to(o.pos);
    j.at("allow_flying").get_to(o.allow_flying);
    j.at("allow_ground").get_to(o.allow_ground);
}

void from_json(const json &j, Artifact &a)
{
    j.at("id").get_to(a.id);
    j.at("name").get_to(a.name);
    j.at("camp").get_to(a.camp);
    j.at("cost").get_to(a.cost);
    j.at("max_cool_down").get_to(a.max_cool_down);
    j.at("cool_down_time").get_to(a.cool_down_time);
    j.at("state").get_to(a.state);
    j.at("target_type").get_to(a.target_type);
}

void from_json(const json &j, CreatureCapacity &c)
{
    j.at("type").get_to(c.type);
    j.at("available_count").get_to(c.available_count);
    j.at("cool_down_list").get_to(c.cool_down_list);
}

void from_json(const json &j, Map &m)
{
    j.at("units").get_to(m.units);
    j.at("barracks").get_to(m.barracks);
    j.at("obstacles").get_to(m.obstacles);
    j.at("ground_obstacles").get_to(m.ground_obstacles);
    j.at("flying_obstacles").get_to(m.flying_obstacles);
    j.at("relics").get_to(m.relics);
}

void from_json(const json &j, Player &p)
{
    j.at("camp").get_to(p.camp);
    j.at("artifact").get_to(p.artifact);
    j.at("mana").get_to(p.mana);
    j.at("max_mana").get_to(p.max_mana);
    j.at("creature_capacity").get_to(p.creature_capacity);
    j.at("newly_summoned_id_list").get_to(p.new_summoned_id_list);
}

} // namespace gameunit

#endif