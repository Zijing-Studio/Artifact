#include "ai_sdk.hpp"
#include "gameunit.hpp"
#include "card.h"

class AI
{
public:
    //选择初始卡组
    void chooseCards()
    {
        // 先获取阵营后选卡组
        json game_info = ai_sdk::read();
        game_info["camp"].get_to(my_camp);
        // artifacts和creatures可以修改
        std::vector<std::string> artifacts = {"HolyLight"};
        std::vector<std::string> creatures = {"Archer", "Swordman", "Priest"};
        ai_sdk::init(my_camp, artifacts, creatures);
    }

    // 更新游戏局面信息
    void updateGameInfo()
    {
        json game_info = ai_sdk::read();
        game_info["round"].get_to(round);
        game_info["camp"].get_to(my_camp);
        game_info["map"].get_to(map);
        game_info["players"][0].get_to(players[0]);
        game_info["players"][1].get_to(players[1]);
    }

    void play()
    {
        if (round < 20)
            ai_sdk::endRound(my_camp, round);
        else
            exit(0);
    }

private:
    int round;
    int my_camp;
    gameunit::Map map;
    gameunit::Player players[2];
};

int main()
{
    AI player_ai;
    player_ai.chooseCards();
    while (true)
    {
        player_ai.updateGameInfo();
        player_ai.play();
    }
    return 0;
}
