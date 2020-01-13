#include <vector>
#include <string>

namespace game
{

struct Unit
{
    int id;
    int camp;
    std::string name;
    cost;
    atk;
    int max_hp;
    int hp;
    atk_range;
    max_move;
    cool_down;
    int pos[3];
    level;
    flying;
    atk_flying;
};

struct Barrack
{
    int pos[3];
    int camp;
    summon_pos_list;
};

struct Relic
{
    int camp;
    int max_hp;
    int hp;
    int pos[3];
    std::string name;
    int id;
};

struct Obstacle
{
    type;
    int pos[3];
    allow_flying;
};

struct Artifact
{
    int id;
    std::string name;
    int camp;
    cost;
    max_cool_down;
    cool_down_time;
    std::string state;
    target_type;
};

struct Creature
{
    std::string type;
    int available_count;
    std::vector<int> cool_down;
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
} // namespace game