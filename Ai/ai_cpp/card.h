#ifndef CARD_H_
#define CARD_H_

namespace card
{
struct Creature
{
    int available_count;
    int cost;
    int atk;
    int max_hp;
    int min_atk_range;
    int max_atk_range;
    int max_move;
    int cool_down;
    bool flying;
    bool atk_flying;
    bool agility;
    bool holy_shield;
    Creature(int _count, int _cost, int _atk, int _maxhp, int _minatk, int _maxatk,
             int _maxmove, int _cool, bool _fly, bool _atkfly, bool _agility,
             bool _holyshield) : available_count(_count), cost(_cost), atk(_atk),
                                 max_hp(_maxhp), min_atk_range(_minatk), max_atk_range(_maxatk),
                                 max_move(_maxmove), cool_down(_cool),
                                 flying(_fly), atk_flying(_atkfly),
                                 agility(_agility), holy_shield(_holyshield) {}
};

struct Artifact
{
    int cost;
    int cool_down;
    Artifact(int _cost, int _cool) : cost(_cost), cool_down(_cool) {}
};

const Creature SWORDMAN[4] = {Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                              Creature(4, 2, 2, 2, 1, 1, 3, 3, 0, 0, 0, 0),
                              Creature(4, 4, 4, 4, 1, 1, 3, 3, 0, 0, 0, 0),
                              Creature(4, 6, 6, 6, 1, 1, 3, 3, 0, 0, 0, 0)};
const Creature ARCHER[4] = {Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            Creature(3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0),
                            Creature(3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0),
                            Creature(3, 2, 1, 1, 2, 4, 3, 4, 0, 1, 0, 0)};
const Creature BLACKBAT[4] = {Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                              Creature(4, 2, 1, 1, 0, 1, 5, 2, 1, 1, 0, 0),
                              Creature(4, 3, 2, 1, 0, 1, 5, 2, 1, 1, 0, 0),
                              Creature(4, 5, 3, 2, 0, 1, 5, 2, 1, 1, 0, 0)};
const Creature PRIEST[4] = {Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                            Creature(4, 2, 0, 2, 0, 0, 3, 4, 0, 0, 0, 0),
                            Creature(4, 3, 0, 2, 0, 0, 3, 4, 0, 0, 0, 0),
                            Creature(4, 5, 0, 3, 0, 0, 3, 5, 0, 0, 0, 0)};
const Creature VOLCANOGRAGON[4] = {Creature(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                   Creature(3, 5, 3, 5, 1, 2, 3, 5, 0, 0, 0, 0),
                                   Creature(3, 7, 4, 7, 1, 2, 3, 5, 0, 0, 0, 0),
                                   Creature(3, 9, 5, 9, 1, 2, 3, 5, 0, 0, 0, 0)};
const Artifact HOLYLIGHT = Artifact(8, 6);
const Artifact SALAMANDERSHIELD = Artifact(6, 6);
const Artifact INFERNOFLAME = Artifact(6, 6);
const Creature INFERNO = Creature(0, 0, 8, 8, 1, 1, 3, 0, 0, 0, 0, 0);

}; // namespace card

#endif