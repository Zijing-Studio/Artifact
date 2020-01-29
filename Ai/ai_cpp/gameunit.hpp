#ifndef GAMEUNIT_HPP_
#define GAMEUNIT_HPP_

#include <vector>
#include <string>
#include "json.hpp"
using json = nlohmann::json;

namespace gameunit
{

typedef std::vector<int> Pos;

struct Unit
{
    int id;
    int camp;
    std::string name;
    int cost;
    int atk;
    int max_hp;
    int hp;
    std::vector<int> atk_range;
    int max_move;
    int cool_down;
    Pos pos;
    int level;
    bool flying;
    bool atk_flying;
    bool agility;
    bool holy_shield;
};

struct Barrack
{
    Pos pos;
    int camp;
    std::vector<Pos> summon_pos_list;
};

struct Relic
{
    int camp;
    int max_hp;
    int hp;
    Pos pos;
    std::string name;
    int id;
};

struct Obstacle
{
    std::string type;
    Pos pos;
    bool allow_flying;
};

struct Artifact
{
    int id;
    std::string name;
    int camp;
    int cost;
    int max_cool_down;
    int cool_down_time;
    std::string state;
    std::string target_type;
};

struct Creature
{
    std::string type;
    int available_count;
};

struct Map
{
    std::vector<Unit> units;
    std::vector<Barrack> barracks;
    std::vector<Relic> relics;
    std::vector<Obstacle> obstacles;
};

struct Player
{
    int camp;
    std::vector<Artifact> artifacts;
    int mana;
    int max_mana;
    std::vector<Creature> creature_capacity;
    std::vector<int> new_summoned;
};

void from_json(const json &j, Unit &u)
{
    j.at("id").get_to(u.id);
    j.at("camp").get_to(u.camp);
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
    j.at("name").get_to(r.name);
    j.at("id").get_to(r.id);
}

void from_json(const json &j, Obstacle &o)
{
    j.at("type").get_to(o.type);
    j.at("pos").get_to(o.pos);
    j.at("allow_flying").get_to(o.allow_flying);
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

void from_json(const json &j, Creature &c)
{
    j.at("type").get_to(c.type);
    j.at("available_count").get_to(c.available_count);
}

void from_json(const json &j, Map &m)
{
    j.at("units").get_to(m.units);
    j.at("barracks").get_to(m.barracks);
    j.at("obstacles").get_to(m.obstacles);
    j.at("relics").get_to(m.relics);
}

void from_json(const json &j, Player &p)
{
    j.at("camp").get_to(p.camp);
    j.at("artifact").get_to(p.artifacts);
    j.at("mana").get_to(p.mana);
    j.at("max_mana").get_to(p.max_mana);
    j.at("creature_capacity").get_to(p.creature_capacity);
    j.at("newly_summoned_id_list").get_to(p.new_summoned);
}

} // namespace gameunit

#endif