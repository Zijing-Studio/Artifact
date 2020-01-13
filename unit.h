#include <vector>
#include <string>

namespace game
{

struct Pos
{
    int x,y,z;
};

struct Unit
{
    int id;
    int camp;
    std::string name;
    int cost;
    int atk;
    int max_hp;
    int hp;
    std::pair<int,int> atk_range;
    int max_move;
    int cool_down;
    Pos pos;
    int level;
    bool flying;
    bool atk_flying;
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