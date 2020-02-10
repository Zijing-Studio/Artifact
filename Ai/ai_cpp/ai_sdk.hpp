#ifndef AI_SDK_HPP_
#define AI_SDK_HPP_

#include <vector>
#include <iostream>

#include "calculator.h"
#include "gameunit.hpp"
#include "json.hpp"
using json = nlohmann::json;

namespace ai_sdk
{
// 通信部分

// 发送字符串长度
void sendLen(std::string s)
{
    int len = s.length();
    unsigned char lenb[4];
    lenb[0] = (unsigned char)(len);
    lenb[1] = (unsigned char)(len >> 8);
    lenb[2] = (unsigned char)(len >> 16);
    lenb[3] = (unsigned char)(len >> 24);
    for (int i = 0; i < 4; i++)
        printf("%c", lenb[3 - i]);
}

// 发送操作
void sendMsg(int player, int round, std::string operation_type, json operation_parameters)
{
    json message;
    message["player"] = player;
    message["round"] = round;
    message["operation_type"] = operation_type;
    message["operation_parameters"] = operation_parameters;
    sendLen(message.dump());
    std::cout << (unsigned char *)(message.dump().c_str());
    std::cout.flush();
}

// 读取信息
json read()
{
    std::string len = "";
    for (int i = 0; i < 4; ++i)
        len += getchar();
    std::string recv_msg = "";
    for (int i = std::stoi(len); i > 0; --i)
        recv_msg += getchar();
    return json::parse(recv_msg);
}

// 玩家player选择初始神器artifacts和生物creatures
void init(int player, std::vector<std::string> artifacts, std::vector<std::string> creatures)
{
    json operation_parameters;
    operation_parameters["artifacts"] = artifacts;
    operation_parameters["creatures"] = creatures;
    sendMsg(player, 0, "init", operation_parameters);
}

// 玩家player在地图[x,y,z]处召唤一个本方类型为type,星级为star的单位
void summon(int player, int round, int type, int star, int x, int y, int z)
{
    json operation_parameters;
    std::vector<int> position = {x, y, z};
    operation_parameters["position"] = position;
    operation_parameters["type"] = type;
    operation_parameters["star"] = star;
    sendMsg(player, round, "summon", operation_parameters);
}

// 玩家player在地图position处召唤一个本方类型为type,星级为star的单位
void summon(int player, int round, int type, int star, std::vector<int> position)
{
    json operation_parameters;
    operation_parameters["position"] = position;
    operation_parameters["type"] = type;
    operation_parameters["star"] = star;
    sendMsg(player, round, "summon", operation_parameters);
}

// 玩家player将id为mover的单位移动到地图[x,y,z]处
void move(int player, int round, int mover, int x, int y, int z)
{
    json operation_parameters;
    operation_parameters["mover"] = mover;
    std::vector<int> position = {x, y, z};
    operation_parameters["position"] = position;
    sendMsg(player, round, "move", operation_parameters);
}

// 玩家player将id为mover的单位移动到地图position处
void move(int player, int round, int mover, std::vector<int> position)
{
    json operation_parameters;
    operation_parameters["mover"] = mover;
    operation_parameters["position"] = position;
    sendMsg(player, round, "move", operation_parameters);
}

// 玩家player令id为attacker的单位攻击id为target的单位
void attack(int player, int round, int attacker, int target)
{
    json operation_parameters;
    operation_parameters["attacker"] = attacker;
    operation_parameters["target"] = target;
    sendMsg(player, round, "attack", operation_parameters);
}

// 玩家player对id为target的目标使用artifact神器
void use(int player, int round, int artifact, int target)
{
    json operation_parameters;
    operation_parameters["card"] = artifact;
    operation_parameters["target"] = target;
    sendMsg(player, round, "attack", operation_parameters);
}

// 玩家player对地图target处使用artifact神器
void use(int player, int round, int artifact, std::vector<int> target)
{
    json operation_parameters;
    operation_parameters["card"] = artifact;
    operation_parameters["target"] = target;
    sendMsg(player, round, "attack", operation_parameters);
}

// 玩家player结束当前回合
void endRound(int player, int round)
{
    json operation_parameters;
    sendMsg(player, round, "endround", operation_parameters);
}

//查询部分

// 己方单位从位置pos_a到位置pos_b的地面距离(考虑被敌方地面生物阻挡但不考虑被敌方生物拦截)
int getDistanceOnGround(gameunit::Map map, gameunit::Pos pos_a, gameunit::Pos pos_b, int camp)
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

// 己方单位从位置pos_a到位置pos_b的飞行距离(考虑被敌方飞行生物阻挡但不考虑被敌方生物拦截)
int getDistanceInSky(gameunit::Map map, gameunit::Pos pos_a, gameunit::Pos pos_b, int camp)
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

// 对于指定位置pos,获取其上所有生物
std::vector<gameunit::Unit> getUnits(gameunit::Map map, gameunit::Pos pos)
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
int checkBarrack(gameunit::Map map, gameunit::Pos pos)
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
bool canUseArtifact(gameunit::Map map, gameunit::Artifact artifact, gameunit::Pos pos, int camp)
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
}; // namespace ai_sdk

#endif