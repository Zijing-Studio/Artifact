#include "ai_sdk.hpp"
#include "gameunit.hpp"

class AI
{
public:
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
            ai_sdk::end(round);
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
    while (true)
    {
        player_ai.updateGameInfo();
        player_ai.play();
    }
    return 0;
}
