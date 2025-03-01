#include <common.h>

unsigned int original_map[] = {
//	RAW_BTN_UP,
//	RAW_BTN_DOWN,
//	RAW_BTN_LEFT,
//	RAW_BTN_RIGHT,
	RAW_BTN_CROSS,
	RAW_BTN_SQUARE,
	RAW_BTN_CIRCLE,
	RAW_BTN_TRIANGLE,
	RAW_BTN_R1,
	RAW_BTN_R2,
	RAW_BTN_L1,
	RAW_BTN_L2,
//	RAW_BTN_SELECT,
	RAW_BTN_START
};

char button[14][2] = {
//	"U",//up
//	"D",//down
//	"L",//left
//	"R",//right
	"*",//cross
	"[",//square
	"@",//circle
	"^",//triangle
	"1",//R1
	"2",//R2
	"1",//L1
	"2",//L2
//	"-",//Select
	"-"//Start
};
unsigned int coords[14][2] = {
//	{20,170},//up
//	{20,190},//down
//	{10,180},//left
//	{30,180},//right
	{80,187},//cross
	{68,180},//square
	{92,180},//circle
	{80,173},//triangle
	{80,160},//R1
	{80,150},//R2
	{20,160},//L1
	{20,150},//L2
//	{45,180},//Select
	{51,180}//Start
};

void draw(int i)
{
   DrawText(button[i], coords[i][0], coords[i][1], 2, 0xffff0000);
}


void DrawButtons(unsigned short * buttons)
{
	unsigned short curr_buttons = *buttons;
	for (int i = 0; i < RAW_BTN_COUNT-5; i++)
	{
		if ((curr_buttons & original_map[i]) == 0)
			draw(i);
		else
			 DrawText(".", coords[i][0]+3, coords[i][1]-2, 2, 0xffff0000);
	}
}

void DrawAnalog(unsigned short * X, unsigned short * Y)
{

    {
    	int Xcoord = ((*X)/9)+9;
    	int Ycoord = ((*Y)/16)+170;
        DrawText(".", Xcoord, Ycoord, 2, 0xffff0000);
    }	
}

void inputDisplay_Main()
{
	if ((gameMode & 0x60000000) == 0)
	{	
		DrawText(".", 23,178, 2, 0xffff0000);

		struct GamepadBuffer * controller = &gamepadSystem->gamepadBuffer[0];
		DrawButtons(&controller->rawController[1]);
		DrawAnalog(&controller->stickLX, &controller->stickLY);
	}
}