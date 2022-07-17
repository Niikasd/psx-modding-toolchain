#include <common.h>

unsigned int original_map[] = {
	RAW_BTN_UP,
	RAW_BTN_DOWN,
	RAW_BTN_LEFT,
	RAW_BTN_RIGHT,
	RAW_BTN_CROSS,
	RAW_BTN_SQUARE,
	RAW_BTN_CIRCLE,
	RAW_BTN_TRIANGLE,
	RAW_BTN_R1,
	RAW_BTN_R2,
	RAW_BTN_L1,
	RAW_BTN_L2,
	RAW_BTN_SELECT,
	RAW_BTN_START
};

char button[14][2] = {
	"U",//up
	"D",//down
	"L",//left
	"R",//right
	"*",//cross
	"[",//square
	"@",//circle
	"^",//triangle
	"1",//R1
	"2",//R2
	"1",//L1
	"2",//L2
	"-",//Select
	"-"//Start
};
unsigned int coords[14][2] = {
	{20,170},//up
	{20,190},//down
	{10,180},//left
	{30,180},//right
	{80,190},//cross
	{70,180},//square
	{90,180},//circle
	{80,170},//triangle
	{75,160},//R1
	{85,160},//R2
	{25,160},//L1
	{15,160},//L2
	{45,180},//Select
	{55,180}//Start
};

void draw(int i)
{
    if ((gameMode & LOADING) == 0)
    {
        DrawText(button[i], coords[i][0], coords[i][1], 2, 0xffff0000);
    }
}


void DrawButtons(unsigned short * buttons)
{
	unsigned short curr_buttons = *buttons;
	for (int i = 0; i < RAW_BTN_COUNT; i++)
	{
		if ((curr_buttons & original_map[i]) == 0)
			draw(i);
	}
}

void inputDisplay_Main()
{
	struct GamepadBuffer * controller = &gamepadSystem->gamepadBuffer[0];
	DrawButtons(&controller->rawController[1]);
}