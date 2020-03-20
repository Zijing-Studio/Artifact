#include "ai_client.h"
#include "card.h"

class AI : public AiClient
{
public:
    //选择初始卡组
    void chooseCards()
    {
        // artifacts和creatures可以修改
        my_artifacts = {"HolyLight"};
        my_creatures = {"Archer", "Swordsman", "Priest"};
        init();
    }

    void play()
    {
        if (round < 20)
            endRound();
        else
            exit(0);
    }
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
