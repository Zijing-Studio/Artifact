#ifndef AI_SDK_HPP_
#define AI_SDK_HPP_

#include <vector>
#include <iostream>

#include "json.hpp"
using json = nlohmann::json;

namespace ai_sdk
{

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

void sendMsg(int round, std::string operation_type, json operation_parameters)
{
    json message;
    message["round"] = round;
    message["operation_type"] = operation_type;
    message["operation_parameters"] = operation_parameters;
    sendLen(message.dump());
    std::cout << (unsigned char *)(message.dump().c_str());
    std::cout.flush();
}

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

void init(std::vector<std::string> artifacts, std::vector<std::string> creatures)
{
    json operation_parameters;
    operation_parameters["artifacts"] = artifacts;
    operation_parameters["creatures"] = creatures;
    sendMsg(0, "init", operation_parameters);
}

void summon(int round, int type, int star, int x, int y, int z)
{
    json operation_parameters;
    std::vector<int> position = {x, y, z};
    operation_parameters["position"] = position;
    operation_parameters["type"] = type;
    operation_parameters["star"] = star;
    sendMsg(round, "summon", operation_parameters);
}

void summon(int round, int type, int star, std::vector<int> position)
{
    json operation_parameters;
    operation_parameters["position"] = position;
    operation_parameters["type"] = type;
    operation_parameters["star"] = star;
    sendMsg(round, "summon", operation_parameters);
}

void move(int round, int mover, int x, int y, int z)
{
    json operation_parameters;
    operation_parameters["mover"] = mover;
    std::vector<int> position = {x, y, z};
    operation_parameters["position"] = position;
    sendMsg(round, "move", operation_parameters);
}

void move(int round, int mover, std::vector<int> position)
{
    json operation_parameters;
    operation_parameters["mover"] = mover;
    operation_parameters["position"] = position;
    sendMsg(round, "move", operation_parameters);
}

void attack(int round, int attacker, int target)
{
    json operation_parameters;
    operation_parameters["attacker"] = attacker;
    operation_parameters["target"] = target;
    sendMsg(round, "attack", operation_parameters);
}

void use(int round, int artifact, int target)
{
    json operation_parameters;
    operation_parameters["card"] = artifact;
    operation_parameters["target"] = target;
    sendMsg(round, "attack", operation_parameters);
}

void use(int round, int artifact, std::vector<int> target)
{
    json operation_parameters;
    operation_parameters["card"] = artifact;
    operation_parameters["target"] = target;
    sendMsg(round, "attack", operation_parameters);
}

void endRound(int round)
{
    json operation_parameters;
    sendMsg(round, "endround", operation_parameters);
}
}; // namespace ai_sdk

#endif