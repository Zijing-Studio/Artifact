#include <string>
#include <vector>
#include <cstdio>

#include "aiclient.h"

class PlayerAi
{
public:
    PlayerAi(json game_info)
    {
        game_info["round"].get_to(round);
        game_info["camp"].get_to(my_camp);
        map = game_info["map"];
        players = game_info["players"];
    }
    void play()
    {
        if (round < 20)
            client.end(round);
        else
            exit(0);
    }

private:
    AiClient client;
    int round;
    int my_camp;
    json map;
    json players;
};

int main()
{
    AiClient client = AiClient();
    while (true)
    {
        json game_info= client.read();
        PlayerAi *ai = new PlayerAi(game_info);
        ai->play();
        delete ai;
    }
    return 0;
}
