
'''
# ParseAndC #
									 R E A D      M E  


     This tool has 3 BIG main vertical windows in the middle and a 4th horizontal one at the bottom.

      ____________________________________________________________________________
     |               <Interpret>|   <Map>   <data offset>|   <file offset boxes>  |
     |__________________________|________________________|________________________|
     |                          |                        |                        |
     |         Original         |        Interpreted     |       Data             |
     |           Code           |            Code        |     Display            |
     |          Window          |           Window       |     Windows            |
     |                          |                        |(Address, Hex and ASCII)|
     |                          |                        |                        |
     |__________________________|________________________|________________________|
     |  some extra information appears here based on the cursor movement          |
     |____________________________________________________________________________|
     |   Indented variable name | Datatype | AddrStart | AddrEnd | valLE | valBE  |
     |                                                                            |
     |                                                                            |
     |____________________________________________________________________________|
     | some options are here.  Make your choice                                   |
     |____________________________________________________________________________|

    -----------------------
   | Original code window  |
    -----------------------

   Here you either type/paste your C structure or variable declaration statements, or you can choose a code file.
   Do not put a .c file that contain other code that are not declarations (macro declarations are OK) as it will give errors.
   So, sanitize your input. Remove all code that is not related with variable declarations.

   Yes, this means a little more work on your part to figure out where all the declarations happened, where all the #defines are etc.
   But, this tool is not about finding those for you - rather, it depends on you being able to feed it the right declarations.

   (I am currently working on where you can just ANY code, not just header files, and the tool will ignore all the function definitions.
   This will make the tool user's job even easier, but the code is not foolproof yet).
   
    --------------------------
   | Interpreted code window  |
    --------------------------

   Once you are satisfied with the content of the Original Code Window, click on the "Interpret" button on top of it.
   It will then compile the code and give you the interpreted result. The main differences you will see (in contrast to the 
   original code window) are:

   a. All the comments have been removed
   b. All the #define instantiations are now resolved. So, if earlier there were statements like
               #define NUM 2
               #define ADD(x,y) x+y
               int intArray[ADD(NUM,3)];
     Now you will see this instead in the Interpreted code window:
               #define NUM 2
               #define ADD(x,y) x+y
               int intArray[2+3];
     Note that it is deliberately NOT showing intArray[5], but be assured that internally it has computed the value. 
     The reason it displays the expression like that is so that you can know what the macro was actually expanded to, and
     also if there was anything wrong with the evaluation of the macro expansion expression.

    Although Tcl/Tk allows you to write on this Interpret code Window, please DO NOT WRITE here. Treat it as read-only.
    It is a bit of pain to make it read-only (redirecting all the key mappings), and I am researching how to do it.
    The only "magic" in this window is when you bring your cursor over the variable names, but before that the "map" must happen.

   Once you can see the interpreted code in the Interpreted code window, the code will still be black-colored - there is no coloring.
   The Coloring only happens if you "map" the code to the data on the right. So, using your mouse, make a selection.
   For all the variable names that fall within that selection, the tool will choose their global-level variables and map them onto the data. 
   For example, suppose you have structs like these defined below, if you just choose f_b (case 2), automatically the global-level variable varB
   will get selected, along with all the variables under it (basically i_b and f_b). Of course, varB is going to be overlapping the
   storage with both i_b and f_b, but that is essentially how structures work. Bottom line is that, if you select ANY part of the structure,
   the whole structure will get selected. This makes sense programmatically too, since usually you read a whole structure.
   
   Also, this tool will completely ignore all variable declarations inside function definitions. For example, if your code is this,
   variable A is selectable for mapping, while variable B is NOT. This is because we only pick up the Global-level variables, 
   and those declared inside function definitions are NOT at the global level.

   int A;
   int main(){
      int B;
   }

   Next, there can be many, many combinations involving whether:

   - The structure is named or not (case 1,2,3,4 have names, but cases 5,6,7,8 do not). In case no name is specified,
     the tool would create a fake struct name like "Anonymous#n", where n is a number.
   - The structure declares any variables along with the definition or not (cases 2,3,6,7 do, but cases 1,4,5,7 do not).
     If no struct variable declaration is specified, the tool will create a fake struct variable like "DummyVar#n", where n is an integer.
     It will not be there in the Interpreted code window, but when you take the cursor on the token right after the closing
     curly brace, the variable description will show this name. The same name will appear in the bottom window too.
   - The structure declares a new type or not (cases 3,4,7,8 do, but cases 1,2,5,6 do not). Usually, when we just create a type using typedef,
     the compiler does not allocate any space on the memory (it only does when a new variable is declared with that created type).
     However, many of the code in production will just have cases 3 or 7, without any later statements like "varC newVar1" or "varG newVar2".
     We could technically ask the tool users to manually add such statements, but then we will lose out on all the nested struct goodies
     that we intend to show. Hence, we came up with a compromise. By default, the tool will treat the typedef statements as regular
     variable declarations, as if they will create the storage on the stack. This behavior can be modified by clicking on the
     "Mapping typedefs too" button (which will then convert to "Don't map typedefs"), or via the command-line option (-t OFF).

    Also remember that we cannot have typedef statements inside a nested struct definition - it must be at the global level.

    Another thing to remember is that in C, even if we define a named struct within another struct (basically, "nested" declaration),
    Then even that nested struct defition becomes global. You cannot define 2 nested structs with the same name. 
    _________________________________________________________________________________________________________________
   |                       |                       |                                |                                |
   |  Case 1               |  Case 2               |  Case 3                        |  Case 4  (not possible)        |
   |_______________________|_______________________|________________________________|________________________________|
   |                       |                       |                                |                                |
   | struct A{             | struct B{             | typedef struct C{              | typedef struct D{              |
   |          int i_a;     |          int i_b;     |                   int i_c;     |                   int i_d;     |
   |          float f_a;   |          float f_b;   |                   float f_c;   |                   float f_d;   |
   |          };           |          } varB;      |                  } varC;       |                  };            |
   |_______________________|_______________________|________________________________|________________________________|

    __________________________________________________________________________________________________________________
   |                       |                       |                                |                                |
   |  Case 5 (nested only) |  Case 6               |  Case 7                        |  Case 8  (not possible)        |
   |_______________________|_______________________|________________________________|________________________________|
   |                       |                       |                                |                                |
   | struct  {             | struct {              | typedef struct {               | typedef struct {               |
   |          int i_e;     |          int i_f;     |                   int i_g;     |                   int i_h;     |
   |          float f_e;   |          float f_f;   |                   float f_g;   |                   float f_h;   |
   |          };           |          } varF;      |                  } varG;       |                  };            |
   |_______________________|_______________________|________________________________|________________________________|


   Once you have made your selection, then click on the "Map" button.
   If you do not make a selection before clicking on the "Map" button, the tool will assume that you chose everything.

   Rush fans will know: The lyrics of the song "Free Will" says: 
 
        "You can choose a ready guide
            In some celestial voice
        If you choose not to decide
            You still have made a choice"

   (Neil Peart, their legendary drummer, died last year, hence this tribute)

    ------------------------
   | Data Display windows:  |
    ------------------------

  Here, there are 3 sub-windows. One for the address, one for the Hex data, one for the ASCII data.
  
  Please treat ALL these subwindows as Read-Only, even though you can actually write in them. Writing will mess things up.
  Just like the Interpreted code window, all the "magic" happens when you bring the cursor over some data that is "mapped".
  A mapped data will be colored with some non-black color.

  There are two offsets associated with the data window. One is the File offset, the other is the Data offset. 
  The default value for both these offsets is 0, and blank indicates 0.

  The File Offset indicates which offset of the file you want to display your 512-byte-wide window from.
  The Data Offset indicates which offset of the file you want to "map" your variable declarations from.

  In other words, if you choose file offset of 8, it will display bytes 8 through 519 (inclusive) in the Hex and ASCII windows.
  Similarly, if you choose Data Offset of 0x10 (or 16 in decimal), it will start coloring the data from the seventeenth byte.

  The File display can be changed via two boxes located right above the Hex Data Window: From Offset [box 1] or [box 2]. 
  The first box is actually a spinbox. Treat the first box as Read-Only. 
  For Page Up / Page Down, click on the spinbox to the right of "From Offset" and use you Up or Down Cursor. Or just use Page Up / Page Down.
  
  Also, once you have mapped your intended variables (they appear as colored to you), you can just double-click on any colored variable.
  That will reposition the data windows (Hex and ASCII) in such a way that the data corresponding to that variable is displayed
  smack right in the middle of the data window. Neat, huh?
  
  You can do the same the other way, too. Just click on any colored data item in either the Hex or Ascii data windows.
  It will immediately scroll the Interpreted code window to the variable corresponding to that data. If multiple variables point to the same data item,
  it will intelligently scroll in such a way that most number of such variables are displayed. Ain't that cool?
  
  If you want to display your file from very specific offset, you can also type it in the Text Box to the right of "or".
  Here you can use human-readable expression, like 1MB-20*5KB+0xADE+(1<<10). Once you are done type, press TAB to focusout.
  When the focusout happens, it will populate the Spinbox with the calculated value, so that you know what value it calculated.

  For the Data Offset, there is only ONE box right above the Interpreted Code Window. There you can enter any human-readable expression,
  and the tool will display it right from that offset. You need to TAB out (focusout) to let the tool know when you are done typing.

    ----------------------------------------------------------------
   | Field Information (based on cursor movement in Data window):   |
    ----------------------------------------------------------------

  This is the main usefulness of this tool. This is located right below the 3 main windows.

  When you hover over a mapped data (or its variable declaration in the Interpreted code window), some extra "Field Information"
  starts appearing in frame below the 3 main windows. These are:

  1. Description: This tells precisely what the compiler thinks the variable type is, what size etc.
  2. Address (start and End): This tell exactly where in the data file (basically the offsets) the variable/data appears. End address is inclusive.
  3. Value (Little-Endian and Big-Endian): For every variable/data, it tells the Little-Endian value and the Big-endian value.
  4. Length: How many bytes this variable occupies.

  Sometimes taking the cursor over the variable/data does not display all these fields, or populates them incorrectly. (This is expected behavior.)
  This usually happens when you have a one-variable-to-many-data (array) or many-variables-to-one-data (union/bitfield) mappings.
  E.g., for array variables, if you take your cursor above the array variable in the Interpreted Code Window, you will see the Description, Address and Length
  fields populated, but not the Value. This is because an array variable contains multiple individual array elements, so displaying an
  "overall" value makes no sense. But, you can always take your cursor to the Data Window and place it on an individual array element -
  then it will properly tell exactly which Array element it is, what its value is, what address etc.
  
  Similarly, for Union or Bitfield, if we place the cursor over the data element in the Data window, all the Value/Addres/Length make no sense.
  Because multiple different-length fields maps to the same data byte(s) in Union, whichever variable in Tck/Tk did get to apply the coloring tag last for
  the same data element will have the last laugh. So, for Union/bitfield, do not look at the "field information" from the Data Window.
  Instead, go to the Interpreted Code Window and place your cursor above the variable name.


    --------------------------------------------------------------------
   | Field Information (NOT based on cursor movement in Data window):   |
    --------------------------------------------------------------------
  
  If you do not care about pointing to any specific data item, but rather want ALL the data items to be listed, this is your place.
 
  This window has line-by-line listing of the different data items. And the listing is hierarchical. Look at the first column (Expand/Collapse)
  Which means, for items like Array and Structure, it will first show only one item - the Array or the Structure.  But, if you then double-click on the item, 
  or hit Enter, or press the Right-Arrow key, or click on the "Expand" icon on the first column, it will expand into Array elements or Structure members.
  
  For example, suppose you see a single entry for an Array item intArray[2]. When you hit enter on this, two more lines will appear below,
  the first one giving the details of the intArray[0] and the second one giving the details of intArray[1].
  
  To navigate, you can use the Arrow keys. Use Up or Down Array keys to go previous or next data items displayed on this window.
  Use the Left and Right arrow to Collapse or Expand a Structure or Array. If you are in the middle of a listed-out Structure memberlist /Array elementlist,
  you can use the Left arrow to go up (or jump) to its parent node (the Structure/Array). Pressing the Left arrow once more will collapse the list.

  There is only a few lines that you can see at the same time (the height of this window is only about 8 lines or so). If you want to see a more
  descriptive listing of ALL the selected variables with their internal members unraveled (expanded), look at the Console that will have a nicely
  formatted listing. The same listing is also provided as a CSV file in the same working directory from where you invoked this tool.
  The default name for this file is snapshot.csv, but you can always change the name by modifying the SNAPSHOT_FILE_NAME variable in the tool.

    --------------------------------------------------------------------
   | Option buttons                                                     |
    --------------------------------------------------------------------
  
   There are a few options here.

   - Mapping Typedefs or not - Sometimes, in production there will be big structures that are typedefed, and later there are variable declarations that use that new type. 
     Now, when you just typedef a variable, the compiler does not create any storage for it since it is just a type. For example, look at the code below:
	 
		typedef struct 
		{
			uint32_t HDDsize;    
			uint32_t sectors;       

			union
			{
				struct
				{
					uint32_t enabled:1;     
					uint32_t field24:1;        
					uint32_t field24_en:1;     
					uint32_t field25:1;        
					uint32_t field25_en:1;     
					uint32_t :0;     
					uint32_t field26:1;        
					uint32_t field26_en:1;     
					uint32_t field27:1;        
					uint32_t field27_en:1;     
					uint32_t reserved:22;   
					uint32_t special_en:1; 
				};
				uint64_t manualCommand;
			};
			
			uint8_t  specialConfiguration[20]; 
		} typeOneEntry_t;
	 
	    typeOneEntry_t newVariable;
	 
	 Suppose we want to map this above structure to some data. 
	 
	 If we select the above code segment in the interpreted code window and map it to the data, the variables inside the typedef will NOT get colored since when you
	 just create a typedef, no storage is created by the compiler. The newVariable will indeed get colored, but that will correspon to 32 bytes of data.
	 So, when you will hover the cursor on top of newVariable, it will show those 32 bytes of data in the Hex and ASCII windows, but no value would be shown.
	 This is not the intended outcome, because we want to see value of the individual fields, like HDDsize, manualCommand, etc. Sure, we can alway go to the bottom window
	 and there expand the tree under newVariable, but that's a bit of work. We want the user to just be able to hover the mouse on top of the structure and see their values.
	 
	 To get this intended outcome, we allow the option of mapping typedefs directly. When you choose that (it is enabled by default), it will treat the newly created type
	 just like a variable declaration, and map it. If you do not want to map the typedefs, click on the "Mapping typedefs too" button, and it will change to
	 "Not mapping typedefs".
	 
     Also to remember - maybe you are using some typedefs that come as part of stdint.h (like uint32_t, uint16_t etc.). It is possible that your code uses a lot of
     these. However, the compiler here does not know what to make of those. In those cases, you have two options: 
	 
       option A. Manually add the typedef statement like "typedef unsigned int uint32_t;" in your code.
       option B. If you are loathe to manually type the typedef statements and would rather do it for once and for all, there is a list inside this tool
       called typedefsBuiltin that already covers a few such cases (like int8_t, int16_t, int32_t, int64_t, uint8_t, uint16_t, uint32_t, uint64_t, intptr_t, uintptr_t).
       If your code uses some other typedefs frequently, maybe you can add them to this list.

   - Debug ON or OFF - when you turn the Debug on, it will start printing a massive amount of debug statements on the console. When you turn it off,
     it will invoke the dumpDetailsForDebug() routine that prints the most important lists and dictionaries used in this tool, and then turns it off.
     So, an easy way to see the internals of this tool for the current code is to turn the Debug ON and OFF one after the other.

##    Running in BATCH mode           ##
  
  If you do not care about the cursor movement, and just want the data to be mapped either on the console or on the CSV file, you can do that too
  by providing the -b (or --batch) option. Alternatively, if you are running it from a terminal (no X-windows) where it is not possible to show any GUI,
  the tool will automatically default to batch mode. In batch mode, only two things are mandatory inputs for command-line: The code and data files. 
  All other options are optional. For a detailed list of options, use the -h (or --help) button.
 
  The GUI version provides a superior experience compared to the batch mode, except one thing that the batch mode can do but the GUI version cannot.
  In the GUI version, you can only select global variables that are contiguous. So, suppose there are 3 structs (A, B and C) defined in your code and
  you only want to map structs A and C, but not B. Since you select a single area using your mouse, it is impossible to exclude B while including A and C.
  However, in the batch mode, you can specificy exactly which all global level variables you want to map by using --global "A C".

  There is a roundabout way of circumventing this, where you may be able to re-arrange the original code so that your intended global variables are contiguous, 
  but there is no guarantee that you can always do that. For example, if you are continuously defining newer structs using older structs, it may not be possible.

	
	python3 ParseAndC.py --help
	sys.version_info(major=3, minor=9, micro=4, releaselevel='final', serial=0) Python 3.x

	The way to invoke this tool is the following:
	
	> python2/3 ParseIT.py [options], where the options are:

	-h, --help                Prints the options available
	-i, --include             followed by a single string that contains the include file path(s), separated by semicolon
	-x, --hex                 Prints the integral values in Hex (default is Decimal)
	-d, --datafile            followed by the data file name
	-c, --codefile            followed by the code file name
	-o, --offset              followed by the offset value (from which offset in the data file the struct will start mapping from)
							  Offsets can be numbers or expressions, but must be then double-quoted, like "3KB+0x12*43-(0o62/0b10)"
	-g, --global              followed by the name of the Global-level variables (or typedefs) that will be mapped
							  If providing multiple variable names, then it must be double-quoted (like "var1 var2")
							  If no variable names are provided, every variable at the global level in the code file will be automatically selected
	-t, --typedef             followed by Yes/No to indicate if typedefs will be mapped as regular variables or not
	-v, --verbose, --debug    to indicate if debug messages will be printed or not
	-b, --batch               to indicate that the tool will run in the non-interactive, non-GUI, terminal batch mode


##     CROSS-PLATFORM STATUS:		##

  This tool is designed to be cross-platform. It is supposed to work anywhere. Since it has minimal dependency, it is not supposed to break.
  
  But the proof of pudding is eating thereof, so we cannot really claim that it works everywhere unless we have actually tested it.

  I have tested it on the following configurations:
  Window 10 Python 2.7
  Window 10 Python 3.8
  Window 7 Python 3.8
  Linux Python 2.7

  For Mac, I could only test it for a few seconds on a colleague's work laptop. For proper testing, I need access to a Mac server. Can any kind soul grant me access?
  Also, access to any Linux testing environment with Python 3 would be appreciated.

  The look and feel of the tool changes as per the OS, but the main tool functionality remains the same.

  It was a royal pain in the ummm... neck porting it from Python 2 to Python 3. You see, at my workplace the predominant Python version is 2.7,
  though it is slowly changing. I googled for changes between Python 2 and Python 3, and it seems reasonable. How wrong I was!!

  There are many, many subtle changes in Python 3 that will break your program written in Python 2. Some examples:
  - Your print used to be a statement, now it is a proper function
  - Your unicode and str were pretty much interchangeable. Now unicode is str, and str is bytes (Uggghhhhh!!)
  - Integer division - Python 2 would return an integer, but Python 3 would return a float
  - dict.key() used to generate a list, now it generates <<class dict_keys>>, so any code expecting it to be a list would fail silently



##     CURRENTLY WORK-IN-PROGRESS:		##
  
  I am currently working on a few items. These items are not fully ready yet:
  - sizeof()
  - bitfield alignemnt for Big-Endian (cannot find a processor to test it).

##     KNOWN ISSUES:		##
  
  This tool is first for me in many ways. 

      - This is my first Python program. 
      - This is my first compiler-writing. 
      - This is my first GUI development of any kind.

  This program has been used extensively by various teams at Intel, and as per their feedback, they are pretty happy.
  
  Still, for a program that contains 12K lines of code,  you can imagine the number of bugs it has!!!

  But, it is the age of outsourcing. So, ALL of you - the potential users - are my testers. I coded this FREE for you, you test this FREE for me. Win-Win!!
  Use it with your own test structures, and report to me anytime anything breaks (see below on how to report a bug).

  I know of an issue. For example, currently it does not handle the const/volatile/static etc. storage qualifier keywords very well.
  However, these storage qualifiers have absolutely no relevance for this too. So, feel free to delete them from your code and rerun it.

##     HOW  TO  REPORT  A  BUG:		##

  Please email to pkmanna AT gmail DOT com with a subject line of "ParseAndC bug" along with the following information/attachments:

  1. Your running environment (Windows / Unix / Mac), Python version.
  2. The input files you used for code and data. If the Data file is large, at least send the Code file. If you typed in the code, copy what you typed.
  3. your Data Offset and File Offset values for which it is breaking.
  4. Turn on the debug setting on this tool by clicking on the "Debug" button . When you do that, the tool will become slow, and it will print a
     whole lot of debug messages on the background console. This is the most useful debugging information, so please capture that and attach it.


##     FEEDBACK PLEASE!!!!		##

  if you like this tool, I want to hear about it.
  If you feel that this tool sucks, I still want to hear about it.
  If you have some feature in mind that you feel would make the tool better, I want to hear about it.

  Please email me with any feedback: pkmanna AT gmail DOT com
  
 ##   FREQUENTLY ASKED QUESTIONS      ##
 
  Q. Why did you need to write your own parser/compiler when open-source solutions (Lex, Yacc, LLVM, Clang) already exist?
  A. Great question. I do admit that I was very much tempted to use them. But then I wanted my tool to be completely self-contained with no dependency.
     If my tool is dependent on other tools, the moment they chnage their API, it will break my tool. I didn't want that to happen.
	 And if you think they will never change their API because so many other tools rely on them, you are sorely mistaken.
	 Just look at what Python did when they moved from 2.x to 3.x - it broke countless Python tools.
	 
  Q. Your Python code does not look very "Pythonic" and looks like C code in many places. Why?
  A. Because it indeed is. I am a C guy, and this is my very first Python program.
  
  Q. Now that you have Open-Sourced it, can I start sending you patches?
  A. I request you to hold off just for a little bit longer for the following reasons:
       a. The tool is still in the Beta stage, and it is not feature-complete. Please allow me some time to add all the other features.
	   b. I have plans to refactor the code.
	   c. I need some more time for doing unit-testing and bug fixes.

'''
##################################################################################################################################
##################################################################################################################################
##
##
## Below is the input structure that I use for demo:
##
demoCode = ['enum { Sun, Mon, Tue};\n', 
'\n',
'//Observe that right now we are also \n',
'//mapping the typedef (can be turned off\n',
'//by clicking on button at the bottom.)\n',
'typedef struct \n',
'{\n',
'    uint32_t HDDsize;\n',
'    uint32_t sectors;\n',
'\n',
'    union\n',
'    {\n',
'        struct\n',
'        {\n',
'            uint32_t enabled:1;\n',
'            uint32_t field24:1;\n',
'            uint32_t field24_en:1;\n',
'            uint32_t field25:1;\n',
'            uint32_t field25_en:1;\n',
'            uint32_t  :0;\n',
'            uint32_t field26:1;\n',
'            uint32_t field26_en:1;\n',
'            uint32_t field27:1;\n',
'            uint32_t field27_en:1;\n',
'            uint32_t reserved:22;\n',
'            uint32_t special_en:1;\n',
'        };\n',
'        uint64_t manualCommand;\n',
'    };\n',
'    \n',
'    uint8_t  specialConfiguration[20];\n',
'} typeOneEntry_t;\n',
'\n',
'#define concat(x,y) x##y\n',
'int concat(a,b);\n',
'\n',
'#define ADD_ONE(x) x+1\n',
'#define if_less_then_add(x,y) (x<y?x:ADD_ONE(y))\n',
'#define BLANK\n',
'#define QUOTE "qu\\"ote"\n',
'#define SUM_UP( i,j) (i+j)\n',
'\n',
'//Use if-then-else by preprocessor\n',
'#define VERSION 1\n',
'\n',
'#if VERSION == 1\n',
'int oldVersion;\n',
'#else\n',
'int newVersion;\n',
'#endif\n',
'int school[2];\n',
'\n',
'//This example shows the interaction of \n',
'//various attributes and #pragma pack(n)\n',
'//The short s is extended to 8 bytes first, \n',
'//but then again brought down to 4 bytes \n',
'//due to #pragma pack(4)\n',
'// Hence we will have the following pads:\n',
'// 3 bytes after char c, 2 bytes after short s\n',
'\n',
'#pragma pack(4)\n',
'\n',
'struct __attribute__((packed)) N2 {\n',
'           char c;\n',
'           short s __attribute__((aligned(8)));\n',
'  } newVar;\n',
'\n',
'/* Thanos did nothing wrong */\n',
'\n',
'struct teacher\n',
'{\n',
'    char teachername[if_less_then_add(2+3,ADD_ONE(7-2)+9)]; // Hi there\n',
'    int salary[ADD_ONE(sizeof(school))];\n',
'}  t1,t2;\n',
'\n',
'\n',
'struct student\n',
'{\n',
'    int roll[SUM_UP(BLANK 0,2+3 BLANK )];\n',
'    //weird is a pointer\n',
'    void **(*(*weird)[6])(char, int);\n',
'    float marks;\n',
'    //weirder is a function, no storage allocated\n',
'    int (*Weirder(const char code)) (int, int) ;\n',
'    int INT[2][3][Tue];\n',
'} st;\n',
'\n',
'\n',
'union U{\n',
'	char CHAR;\n',
'	short SHORT;\n',
'	float FLOAT;\n',
'} u;\n',
'\n',
'typedef struct student STUDENT_TYPE, *POINTER_STUDENT_TYPE;\n',
'typedef POINTER_STUDENT_TYPE ARRAY_POINTER_STUDENT_TYPE[3];\n',
'ARRAY_POINTER_STUDENT_TYPE pStudent, *ppStudent;\n',
'\n',
'typedef int (*INT)[2](int), *pINT;              \n',
'typedef INT ppINT, *INT2[3];                    \n',
'INT2 i[5];\n',
'ppINT * typedefI1, **typedefI2[5];\n',
'\n',
'\n']
##
##
##
##
##
##



#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import re
from collections import OrderedDict 


################################################################################################################################
# Changelog :   
################################################################################################################################
#
# 2019-09-05 - findTokenListInLines() now working for match occurring over multiline inputLine
#				Also macro substitution seems to be working OK
# 2019-09-06 - Now added '##' operator
# 2019-09-06 - fixed a bug in the parseArithmeticExpression that did not handle the Right-to-Left associativity
# 2019-09-16 - Realized that we cannot ERROR out for the AST-->String routine in case the output string does not parse into the same input AST
#              (because the input AST may not be properly parenthesized). So changed it to a WARNING instead.
# 2019-09-23 - Added code on how to interpret a variable declaration
# 2019-10-13 - This version has the GUI integration done, and interpretation is happening properly. This is before I attempt to add the Focus part.
# 2019-10-18 - This version has the mapping working, typedef done. Before I try to remove the encoding stuff.
# 2019-10-19 - Now the selection part is working. Before adding messagebox
# 2019-10-23 - Did upto parseArithmeticExpression (including evaluateArithmeticExpression), outputTextArithmeticExpressionFromAST
# 2019-11-28 - Now added cursor movement on data window too.
# 2019-12-03 - Split the variableDescription into a dictionary named variableDescriptionExtended, with various keys of "description", "signedOrUnsigned", "datatype", "arrayDimensions", "arrayElementSize" 
# 2019-12-04 - Now added bitwise field support in internal value calculations (not in variable declaration yet)
# 2019-12-15 - Now added highlighting of individual array elements
# 2019-12-15 - Split the value into Little-Endian and Big-Endian parts
# 2019-12-17 - Added highligthing all around, fixed bugs regarding enum and function declarations. Next up: typedef resolution (properly)
# 2019-12-22 - This is the version after which we will split the structure defining part completely. Not that the current form works completely.
# 2019-12-23 - Nested structure now seem to be working. Next need to work on the Union.
# 2019-12-24 - Included new fields added to the variableDescriptionExtended. This is just after we removed the 6-th element of variableDescription, which is now variableDescriptionExtended["globalTokenListIndex"] (recall variableDescriptionExtended itself is item[4])
# 2019-12-24 - Now we are going to change the coloring based on self.dataOffsetsDetail rather than self.dataOffsetsDetail.
# 2019-12-24 - I think Union is now working.
# 2019-12-28 - Now the compiler padding addition is working. For size, we need to use the base datatype for array variables.
# 2019-12-29 - Now typedef is working, but the global index of variable (globalTokenListIndex) is only correct if we have a single variable declared within the declaration statement.
# 2019-12-29 - Now typedef is working, but only if the original typedef statement created a single type. Now going to change that
# 2019-12-30 - Typedef now works for multiple-variable declarations, as well as multiple-type-creation-in-a-single-typedef statement
# 2019-12-31 - Transitioned to PRINT, revamped the type specifier part (no conflicting float/int/char etc.) now going to implement bitfields.
# 2020-01-01 - Added code to convert human-readable (GB/MB) etc. to decimal. Next intend to change the offset entry variables.
# 2020-01-02 - Added currentDeclarationSegmentStartIndex, currentDeclarationSegmentEndIndexInclusive, and initializationStartIndex to variableDescriptionExtended{} so that declaration segment identification is easier.
# 2020-01-02 - Before we start changing the way the validate and focusout routines work
# 2020-01-03 - Before we split up the Interpreted code display
# 2020-01-04 - Fixed a bunch of bugs regarding changing the data offset (causes the self.dataOffsetsDetail need to be redone) and file offset (causes the block to be re-read)
# 2020-01-05 - Fixed the operator precedence bug in parseArithmeticExpression() where - should have higher precedence than +
# 2020-01-05 - Fixed enum variable declaration bug (still not ready for typedef enum)
# 2020-01-09 - Just added the bitfield information dictionary into the sruct component and did the overall size calculation. Now will work on the display etc.
# 2020-01-13 - Bitfield now working for LE packing
# 2020-01-14 - replaced all checks for isinstance( -x-, basestring) with checkIfString( -x- ) since basestring is no longer available in Python 3
# 2020-01-18 - Before replacing *.keys() with getKeyList(*). This is because Python 2 gets *.keys() as a list, but Python 3 gets *.keys as class dict_keys (Ugghhh!)
# 2020-01-18 - Now the "Interpret" is working. But map is failing due to byte-vs-Str mismatch (various invocation of ord() function)
# 2020-01-19 - Now the map is working too, because earlier it was failing due to Integer division not working in Python 3. 
# 2020-01-20 - Added README. After fixing the multi-window display data
# 2020-01-23 - Before adding the fourth Window (created a barebone unraveled list). Next going to add the TreeView
# 2020-01-23 - Now treeview is working somewhat.
# 2020-01-27 - Before trying to use the same offsets from the offsetDetails. Now this fixed some bugs regarding functions.
# 2020-01-27 - After trying to use the same offsets from the offsetDetails. Also fixed the bug in mapStructure where populateDataMap() was getting called before performInterpretedCodeColoring()
# 2020-01-28 - The Address start and end in the 4th Window now working. Also, fixed the bug in previously not using removeColorTags() so that if we now re-choose, previous colors remain.
# 2020-01-28 - Now the inserting-into-typedef part has been moved into where it should belong (parseVariableDeclaration() function). Corresponding code in parseStructre() and parseCodeSnippet() are now commented out.
# 2020-01-28 - Fixed the bug where I was not deducting the offset while reading from the blockRead in populateDataMap(). Previous versions would give wrong result.
# 2020-01-29 - Now even struct members can use derived type declarations.
# 2020-01-29 - Now variable description is also part of unravel, so it can decode any kind of value. Next will display the bytes for each field.
# 2020-01-29 - Now byte values are showing too in the tree view. Next optional Hex display and pretty printing.
# 2020-01-29 - mandatory Pretty printing of unraveled done. Also fixed small cosmetic bug of extra period on struct name.
# 2020-01-30 - Now optional ability to display all integral values in Hex is added.
# 2020-02-02 - BitField now working. Before merging the Big-endian and Little-endian.
# 2020-02-03 - Merged the Big-endian and Little-endian, and also fixed the bug where a single field might be broken at the beginning or the end of the block.
# 2020-02-10 - Now it supports sizeof() for simple expressions.
# 2020-02-12 - Before changing the code so that unraveling doesn't happen only for a file offset change
# 2020-02-12 - Now unraveling doesn't happen only for a file offset change. Now going to clear up the dataOffset and fileOffset naming mess.
# 2020-02-13 - Renamed self.dataOffsets to self.variableOffsets and self.dataOffsetsDetail to self.variableOffsetsDetail.
# 2020-02-14 - Fixed many small things to make sure it runs on both Python 2 and 3.
# 2020-02-21 - Added the second (faster) routine for findTokenListInLines. Now going to fix the problem of the Data windows getting double-written. 
# 2020-02-24 - Fixed the bug of Interpreted Code Window variable highlighting remaining in case of Page Up and Down.
# 2020-02-29 - Added code to support builtin typedefs.
# 2020-03-02 - Now showing addresses for bitfields.
# 2020-03-04 - Fixed enum bug where it was not halding expressions. Also added handling of storage qualifiers like volatile.
# 2020-03-06 - After adding the Hex / Dec toggle feature.
# 2020-03-07 - After adding Command line parser, and before preparing for the batch mode.
# 2020-03-08 - From GUI variables, made these variables global: dataLocationOffset, dataFileName, dataFileSizeInBytes, and block
# 2020-03-09 - From GUI variables, made these variables global: variableOffsets, variableOffsetsDetail
# 2020-03-09 - From GUI variables, made these variables global: inputIsHexChar, binaryArray, hexCharArray, totalBytesToReadFromDataFile
# 2020-03-09 - Removed commented out lines due to all those Global-making endeavor.
# 2020-03-13 - Before doing the massive restructuring.
# 2020-03-15 - After doing the massive restructuring. Still, when self.fileOffset changes, excess things are happening. 
# 2020-03-15 - Before committing to use fileDisplayOffset instead of self.fileOffset.
# 2020-03-16 - After adding code to selectively choose whether to display typedefs or not. Before adding bottom line of options.
# 2020-03-17 - Everything seems to be working. Removed the inefficient version of findTokenListInLines().
# 2020-03-18 - Now Help option and batch mode are working.
# 2020-03-22 - Fixed padding bug. Added more content to README. Removed a lot of commented out lines.
# 2020-03-25 - Added support for #pragma pack. Just parsed __attribute__(( options )), but yet to take any action.
# 2020-03-27 - Before processing packed and aligned __attribute__.
# 2020-03-29 - Added a lot of comments and illustrations regarding packed and aligned __attribute__. Yet to add the code for detecting __attribute__ properly.
# 2020-04-10 - Now it parses the aligned and packed properly, but yet to take action on those attributes.
# 2020-04-23 - Now it properly implements the packed and aligned attributes. Next we will implement the bitfields correctly (previous implementation was incorrect).
# 2020-04-27 - Previous implementation was wrong. Re-did the packed, aligned, and pragma pack. Bitfield still not done.
# 2021-03-19 - Fixed bug that was causing the program to crash when trying to tab out of the data offset with a blank datablock.
# 2021-03-29 - Changed tokenizeLines to also create precise token locations. Now going to return both items instead of just tokenList.
# 2021-03-29 - The new code now gets both tokenList and precise token locations from tokenlizeLines(). It does not use the latter though. Next we will handle ifdefs.
# 2021-04-04 - After handling preprocessing directives. But going to rewrite the tokenizeLines(), so this backup is just before that.
# 2021-04-05 - Reimplemented tokenizeLines() that correctly handles all preprocessing directives. This is before handing <include "filename"> statements.
# 2021-04-05 - Reimplemented preProcess() that now handles <include "filename"> statements.
# 2021-04-06 - Added feature of centering Data window based on double-clicked variable name.
# 2021-04-06 - Added routine displayDataWindowFromOffset(), which is used by page up/down and doubleclick (refactored the code)
# 2021-04-06 - Added more stuff into displayDataWindowFromOffset(), by taking commong things away from page up/down and doubleclick (refactored the code)
# 2021-04-08 - Added support for variadic macro. Next going to add support for INCLUDE_FILE_PATH
# 2021-04-19 - Before putting in a "Demo" mode
# 2021-04-21 - Before renaming the Compiler Padding on to Demo
# 2021-04-22 - Before adding the Expand/Collapse buttons on the bottom TreeView window
# 2021-04-26 - After adding code to handle function definitions (not declarations), and removing structure-end-padding button. Before removing extra refernces.
# 2021-04-28 - Changed the builtin code used for Demo.
# 2021-04-29 - Added Double-click feature for the Hex and Ascii data windows.
# 2021-05-05 - Added zero-width bitfield variable (alignment reset) handling

# Global settings

IN_DEMO = False			# Runs a demo using some fixed code and data
BATCHMODE = False
PRINT_DEBUG_MSG = False		# use True or False ony
HIGHLIGHT_COLOR = "black"	# "black" or "yellow" works better
COMPILER_PADDING_ON = True
STRUCT_END_PADDING_ON = True	# Whether to add additional padding at the end of a structure to make to align to a word boundary
DISPLAY_INTEGRAL_VALUES_IN_HEX = False	#If True, -17 would now be displayed as -0x11
SNAPSHOT_FILE_NAME = "snapshot.csv"		# This is the output file name where the formatted data snapshot would be written in the current folder
MAP_TYPEDEFS_TOO = True	# Usually, we do not create any storage for typedef (so no mapping), but if that's all your structure has and you do not want to create extra declaration, turn it to True

anonymousStructPrefix = "Anonymous#"
dummyVariableNamePrefix = "DummyVar#"
dummyZeroWidthBitfieldNamePrefix = "DummyZeroWidthBitfieldVar#"


CHAR_SIZE = 1
SHORT_SIZE = 2
INT_SIZE = 4
LONG_SIZE = 4
LONG_LONG_SIZE = 8
POINTER_SIZE = 4
FLOAT_SIZE = 4
DOUBLE_SIZE = 8
BITS_IN_BYTE = 8

ALIGNED_DEFAULT_VALUE = 4

LITTLE_ENDIAN = 0
BIG_ENDIAN = 1

# The start and end addresses (byte numbers) for bitfields change based on whether we are packing LE or BE. Change it accordingly.
BITFIELD_DEFAULT_ENDIANNESS = LITTLE_ENDIAN		
#BITFIELD_DEFAULT_ENDIANNESS = BIG_ENDIAN		

storageClassSpecifier = [ 'auto','register','static','extern','typedef']
typeQualifier = ['const','volatile']

# These are the typedefs that will be used if the user fails to explicitly typedef them.
typedefsBuiltin = {
					'int8_t'	:	['typedef', 'char', 'int8_t', ';'],
					'int16_t'	:	['typedef', 'short', 'int16_t', ';'],
					'int32_t'	: 	['typedef', 'int', 'int32_t', ';'],
					'int64_t'	: 	['typedef', 'long long', 'int64_t', ';'],

					'uint8_t'	:	['typedef', 'unsigned', 'char', 'uint8_t', ';'],
					'uint16_t'	:	['typedef', 'unsigned', 'short', 'uint16_t', ';'],
					'uint32_t'	: 	['typedef', 'unsigned', 'int', 'uint32_t', ';'],
					'uint64_t'	: 	['typedef', 'unsigned', 'long long', 'uint64_t', ';'],

					'intptr_t'	:	['typedef', 'int', '*', 'intptr_t', ';'],
					'uintptr_t'	:	['typedef', 'unsigned', 'int', '*', 'uintptr_t', ';']
					}

# Put all your include filepaths separated by semicolon here
INCLUDE_FILE_PATHS = r"C:\Users\yourName\Documents\INCLUDE_FILE_DIR"

sys.stdout.write(str(sys.version_info))
PYTHON2x = True if (sys.version_info >= (2, 7, 0) and sys.version_info < (3, 0, 0)) else False
PYTHON3x = True if sys.version_info >= (3, 0, 0) else False

if PRINT_DEBUG_MSG != True and PRINT_DEBUG_MSG != False:
	sys.stdout.write("PRINT_DEBUG_MSG must be either True or False - exiting!")
	sys.exit()

if BATCHMODE not in (True, False):
	sys.stdout.write("BATCHMODE must be either True or False - exiting!")
	sys.exit()

#print (PYTHON2x)
#print (PYTHON3x)

if DISPLAY_INTEGRAL_VALUES_IN_HEX not in (True, False):
	sys.stdout.write("Currently, DISPLAY_INTEGRAL_VALUES_IN_HEX is NOT either True or False (must be one of them) - exiting!\n") 
	sys.exit()
	
if PYTHON2x and PYTHON3x:
	sys.stdout.write("BAD Coding, dummy!!! How come both Python 2 and Python 3 indicators are True?\n") 
	sys.exit()
elif not PYTHON2x and not PYTHON3x:
	sys.stdout.write("Unsupported version of Python!")
	sys.stdout.write(sys.version_info)
	sys.exit()
else:
	if PYTHON2x:
		sys.stdout.write(" Python 2.x\n" )
	if PYTHON3x:
		print (" Python 3.x\n")

if BITFIELD_DEFAULT_ENDIANNESS not in (LITTLE_ENDIAN, BIG_ENDIAN):
	sys.stdout.write("\nDefault value of BITFIELD_DEFAULT_ENDIANNESS must be either LITTLE_ENDIAN or BIG_ENDIAN\n" )
	sys.exit()

if MAP_TYPEDEFS_TOO not in (True, False):
	sys.stdout.write("\nDefault value of MAP_TYPEDEFS_TOO must be either True or False\n" )
	sys.exit()

if len(anonymousStructPrefix.strip()) <2 or anonymousStructPrefix[-1] != "#":
	sys.stdout.write("\nanonymousStructPrefix must end with a \"#\" to ensure that it does not clash with a real struct/Union name\n" )
	sys.exit()
if len(dummyVariableNamePrefix.strip()) <2 or dummyVariableNamePrefix[-1] != "#":
	sys.stdout.write("\ndummyVariableNamePrefix must end with a \"#\" to ensure that it does not clash with a real variable name\n" )
	sys.exit()

def ORD(inputStr):
	if PYTHON2x:
		return ord(inputStr)
	elif PYTHON3x:
		if isinstance(inputStr,str):
			return ord(inputStr)
		elif isinstance(inputStr,(bytes,int)):
			return inputStr
		else:
			sys.stdout.write("ERROR in coding: Attempting to extract ordinal value from non-string object of type",type(inputStr))
			sys.exit()
	else:
		sys.stdout.write("Unsupported version of Python - ord() unavailable!")
		sys.exit()

def HEX(n):
	if not checkIfIntegral(n):
#		sys.stdout.write ("\nInside HEX: Input is NOT integral, Input type = ")
#		sys.stdout.write (str(type(n)))
		return n
	elif n < 0:
#		sys.stdout.write ("Inside HEX: Negative")
		return "-0x"+("%x"%(-n)).upper()
	else:
#		sys.stdout.write ("Inside HEX: Positive")
		return "0x"+("%x"%(n)).upper()
	
	
def checkIfBoolean(inputStr):
	if type(inputStr) == type(True):
		return True
	else:
		return False

# Python changed in v3 
def checkIfString(inputStr):
#	print ("inputStr = ", inputStr)
#	print ("type(inputStr) = <%s>"%type(inputStr))
	if PYTHON2x and isinstance(inputStr,basestring):
		return True
	elif PYTHON3x and isinstance(inputStr,str):
		return True
	else:
		return False

def checkIfIntegral(inputStr):
#	print ("inputStr = ", inputStr)
#	print ("type(inputStr) = <%s>"%type(inputStr))
	if PYTHON2x and (isinstance(inputStr,int) or isinstance(inputStr,long)):
		return True
	elif PYTHON3x and isinstance(inputStr,int):
		return True
	else:
		return False


# This checks if the input is either a string, or a list comprised of similar lists and strings only
def checkIfStringOrListOfStrings(input):
#	print ("input = ", input)
#	print ("type(input) = <%s>"%type(input))
	if isinstance(input,list):
		for item in input:
			if not checkIfStringOrListOfStrings(item):
				return False
		return True
	else:
		return checkIfString(input)

# Do NOT use this function to convert things that are NOT supposed to be strings (like bytes)
def convert2Str(input):
	if checkIfString(input):
		return input
	elif isinstance(input,list):
		outputList = []
		for item in input:
			outputList.append(convert2Str(item))
		return outputList
	elif isinstance(input,dict):
		outputDictionary = {}
		for key, value in input.iteritems():
			strKey = convert2Str(key)
			strValue = convert2Str(value)
			outputDictionary[strKey] = strValue
		return outputDictionary
	elif PYTHON3x and isinstance(input,bytes):
		return input.decode("ascii","ignore")
	elif PYTHON2x and isinstance(input,unicode):
		return str(input)
	else:
		PRINT ("EARNING: unhandled case for input = <",input,">")
		return input

#######################################################################################################################################################
#This returns the flattened version of an input List (just imagine the list without ALL the inside [] )
#######################################################################################################################################################

def flattenList(inputList):
	if checkIfString(inputList):
		return inputList
	elif isinstance(inputList,list):
		if len(inputList) == 1:
			return inputList
		else:
			returnList = []
			for item in inputList:
				temp = flattenList(item)
				if isinstance(temp,list):
					returnList.extend(temp)
				else:
					returnList.append(temp)
			return returnList
	else:
		return inputList

#inputList = [["a1","+","b2"],"*",["c3","/","d4"],"+","e5"]
#flattened = flattenList(inputList)
#print flattened

#sys.exit()

#######################################################################################################################################################
#This returns the string version of an input List (just imagine the list without the surrounding [] and the comma separators)
#######################################################################################################################################################

def list2plaintext(inputList):
	if checkIfString(inputList):
		return inputList
	elif isinstance(inputList,list):
		returnValue = ""
		for i in range(len(inputList)):
			if i>0:
				returnValue += " "
			returnValue += list2plaintext(inputList[i])
		return returnValue
	else:
		return False

#######################################################################################################################################################
#This returns the index of the first occurrence of a contiguous sequence of items in a list (like finding a substring in a string)
#######################################################################################################################################################
def findIndexOfSequenceInList(sequence,inputList):
	if checkIfString(inputList) and checkIfString(sequence):
		return inputList.find(sequence)
	if not isinstance(inputList,list):
		return False
	if checkIfString(sequence):
		sequence = [sequence]
	
	for i in range(len(inputList)-len(sequence)+1):
		if inputList[i:i+len(sequence)] == sequence:
			return i
	
	return -1


#######################################################################################################################################################
#This returns the string version of an input dictionary
#######################################################################################################################################################
def dictionary2string(inputDictionary):
#	PRINT ("inside dictionary2string, inputDictionary =", inputDictionary )
	if isinstance(inputDictionary,int):
		return str(inputDictionary)
	elif PYTHON2x and isinstance(inputDictionary,long):	# This is only for Python 2.x
		return str(inputDictionary)
	elif isinstance(inputDictionary,float):	
		return str(inputDictionary)
	elif checkIfString(inputDictionary):
		return "'"+inputDictionary+"'"
	elif isinstance(inputDictionary,list):
		return list2string(inputDictionary)
	elif isinstance(inputDictionary,dict):
		dictionaryLength = len(inputDictionary)
		itemCount = 0
		outputStr = '{'
		for key in inputDictionary.keys():
			outputStr += dictionary2string(key)+": "+dictionary2string(inputDictionary[key])
			if itemCount < dictionaryLength-1:
				outputStr += ', '
			itemCount += 1
		outputStr += '}'
#		PRINT ("returning outputStr =",outputStr )
		return outputStr
	elif inputDictionary == None:
		return "None"
	else:
		print ("ERROR in dictionary2string() - unknown type", inputDictionary, "while expecting a dictionary" )
		sys.exit()
		
#######################################################################################################################################################
#This returns the string version of an input List
#######################################################################################################################################################
def list2string(inputList):
#	PRINT ("inside list2string, inputList =", inputList )
	if isinstance(inputList,int):
		return str(inputList)
	elif PYTHON2x and isinstance(inputList,long):	# This is only for Python 2.x
		return str(inputList)
	elif isinstance(inputList,float):	
		return str(inputList)
	elif checkIfString(inputList):
		return "'"+inputList+"'"
	elif PYTHON3x and isinstance(inputList,bytes):
		return "'"+inputList.decode("utf-8")+"'"
	elif isinstance(inputList,dict):
		return dictionary2string(inputList)
	elif isinstance(inputList,list):
		outputStr = '['
		for i in range(len(inputList)):
			outputStr += list2string(inputList[i])
			if i < len(inputList)-1:
				outputStr += ', '
		outputStr += ']'
#		PRINT ("returning outputStr =",outputStr )
		return outputStr
	elif inputList == None:
		return "None"
	else:
		print ("ERROR in list2string() - unknown type", inputList, "while expecting a list" )
		sys.exit()

##########################################################################################################################################################
# We do not know if the output of the str() function would change in different Python versions, hence here is our own custom "convert-to-string" routine
##########################################################################################################################################################
def STR(input):
	if checkIfString(input):
		return input
	elif isinstance(input,list):
		return list2string(input)
	elif isinstance(input,dict):
		return dictionary2string(input)
	else:
		if PYTHON2x:
			return str(input)
		elif PYTHON3x:
			if isinstance(input,(bytes, bytearray)):
				return input.decode("ascii","ignore")
			else:
				return str(input)
		else:
			print ("ERROR in STR() - Should never come here")
	


##########################################################################################################################################################
# Universal PRINT function
##########################################################################################################################################################
def PRINT (*argv):
	printString = ""
	for arg in argv:
		strArg = STR(arg)
		printString += strArg + (" " if len(strArg)>0 and strArg[-1] != "\n" else "")
	if PRINT_DEBUG_MSG:
		print (printString)

##########################################################################################################################################################
# PRINT function that will always work, irrespective of the value of PRINT_DEBUG_MSG
##########################################################################################################################################################
def MUST_PRINT (*argv):
	global PRINT_DEBUG_MSG
	backedUpValuePRINT_DEBUG_MSG = PRINT_DEBUG_MSG
	PRINT_DEBUG_MSG = True
	printString = ""
	for arg in argv:
		strArg = STR(arg)
		printString += strArg + (" " if len(strArg)>0 and strArg[-1] != "\n" else "")
	if PRINT_DEBUG_MSG:
		print (printString)
	PRINT_DEBUG_MSG = backedUpValuePRINT_DEBUG_MSG
	
##########################################################################################################################################################
# PRINT function that will always work, irrespective of the value of PRINT_DEBUG_MSG
# The reason we have this separate OUTPUT function is the follows. We intend to use MUST_PRINT mostly for debugging selective statement,
# as setting the PRINT_DEBUG_MSG = True will turn on the debug globally and flood the console. So, for selective debug, a better approach is to
# take the existing PRINT statement, and then convert them to MUST_PRINT() function. That way, only those MUST_PRINT statements will print, while the
# rest of the regular PRINT() statements won't. Then when the debugging is over, replace those MUST_PRINT() back to ordinary PRINT() statement.
#  
# The only problem with this approach is that there are certain MUST_PRINT() statements that are not for debugging, but rather for regular business.
# For example, in the console we also lay out the structure with field values. Now, if we use MUST_PRINT() statement for those too, the a user
# who is using a "replace-all" for replacing MUST_PRINT() into PRINT() will also end up replacing those statements which were not for debugging at all.
# To avoid this confusion, we use another function OUTPUT which should be strictly used for "regular", non-debug must-print requirements.
##########################################################################################################################################################
OUTPUT = MUST_PRINT

PRINT ("version is " )
PRINT (sys.version_info )


#################################################################################################################################################
# Python changed they way they output the dict.keys() function. In Python 2, the output type is a list. In Python 3, it is a dict_keys object.
# So, if you have a statement like "for key in someDict.keys()", that will work in both Python 2 and 3, since the "key" value is same.
# However, suppose you want to extract the list of keys into a list, and then start want to do some operations on that list expecting it to be a "list" object.
# For example, suppose you have "if item in someDict.keys()". That will fail in Python 3, since it is no longer a list object, but a dict_keys object.
# Hence, we are putting a wrapper that will force it to be a list for Python 3.
#################################################################################################################################################
def getDictKeyList(inputDict):
	if not isinstance(inputDict, dict):
		OUTPUT ("ERROR - input to this function is NOT a dictionary",inputDict)
		sys.exit()
	elif not inputDict:
		return []
	elif PYTHON2x:
		return inputDict.keys()
	elif PYTHON3x:
		keyList = list(inputDict.keys())
		if not isinstance(keyList, list):
			OUTPUT ("ERROR in coding - output is still not a list",keyList)
			sys.exit()
		else:
			return keyList
	else:
		PRINT ("Sorry, only Python 2.7 and above are supported now")
		sys.exit()
		
		
try:
	if sys.version_info >= (3, 0, 0):
		PRINT ("For Python 3.0 and above ..." )
		import tkinter as tk
		import tkinter.ttk as ttk
		import tkinter.filedialog as filedialog
		from tkinter import messagebox as messageBox
	elif sys.version_info >= (2, 7, 0):
		PRINT ("For Python 2.7 and above (but below Python 3.0)" )
		import Tkinter as tk
		import ttk
		import tkFileDialog as filedialog
		import tkMessageBox as messageBox
	else:
		# Do 2.6+ stuff
		PRINT ("Unknown version - exiting" )
		sys.exit()
	try:
		Spinbox = ttk.Spinbox
	except AttributeError:
		Spinbox = tk.Spinbox
#except ModuleNotFoundError:		# Works only on Python 3, not 2
except ImportError:
	OUTPUT ("Cannot instantiate tkinter - going into batch mode")
	BATCHMODE = True



def integerDivision(a,b):
	if sys.version_info >= (3, 0, 0):
		if isinstance(a,int) and isinstance(b,int):
			returnValue = a // b
		else:
			PRINT ("WARNING: Inputs to integerDivision(",a,",",b") are not integral") 
			returnValue = a / b
	else:
		returnValue = a / b
	return returnValue


# Given a bit number, this returns the corresponding byte number
def bit2Byte (bitNumber):
	if not checkIfIntegral(bitNumber):
		sys.stdout.write ("Input to bit2Byte() is not integral - exiting")
		sys.exit()
	elif bitNumber < 0:
		sys.stdout.write ("Input to bit2Byte() cannot be negative - exiting")
		sys.exit()
	else:
		return integerDivision(bitNumber,BITS_IN_BYTE)
		
# Given a byte number, this returns the first bit number corresponding to that byte number
def byte2Bit (byteNumber):
	if not checkIfIntegral(byteNumber):
		sys.stdout.write ("Input to byte2Bit() is not integral - exiting")
		sys.exit()
	elif byteNumber < 0:
		sys.stdout.write ("Input to byte2Bit() cannot be negative - exiting")
		sys.exit()
	else:
		return byteNumber * BITS_IN_BYTE

# Global variables

TOOL_NAME = "ParseAndC by Parbati Kumar Manna"
DISPLAY_BLOCK_WIDTH = 16
DISPLAY_BLOCK_HEIGHT = 32
BLOCK_SIZE = DISPLAY_BLOCK_WIDTH * DISPLAY_BLOCK_HEIGHT
ENCODINGS = ("ASCII", "CP037", "CP850", "CP1140", "CP1252", "Latin1", "ISO8859_15", "Mac_Roman", "UTF-8", "UTF-8-sig", "UTF-16", "UTF-32")
#When you have no more than 10 colors, use this
COLORS_10 = ['red2','SkyBlue1', 'magenta2','saddle brown', 'cornflower blue','dark green', 'deep pink', 'purple','chocolate1','gold']
COLORS_20 = ['red2','SkyBlue1', 'magenta2','saddle brown', 'cornflower blue','dark green', 'deep pink', 'purple','chocolate1','gold',
'DarkGoldenrod2', 'DarkOrange1', 'plum1','DarkOrchid1', 'DeepPink2', 'DeepSkyBlue2', 'orange', 'DodgerBlue2','turquoise','indian red']
COLORS_ALL = ['DarkGoldenrod2', 'DarkOrange1', 'DarkOrchid1', 'DeepPink2', 'DeepSkyBlue2', 'DodgerBlue2', 
'HotPink1', 'IndianRed1', 'LightPink1', 'LightSalmon2', 'MediumOrchid1', 'MediumPurple1', 'OrangeRed2', 
'PaleVioletRed1', 'RoyalBlue1', 'SeaGreen1', 'SkyBlue1', 'SlateBlue1', 'SpringGreen2', 'SteelBlue1', 'VioletRed1', 
'blue', 'blue violet', 'brown1', 'cadet blue', 'chartreuse2', 'chocolate1', 
'coral', 'cornflower blue', 'cornsilk2', 'cyan', 'dark goldenrod', 'dark green', 'dark khaki', 'dark olive green', 'dark orange', 'dark orchid', 'dark salmon', 
'dark sea green', 'dark slate blue', 'dark slate gray', 'dark turquoise', 'dark violet', 'deep pink', 'deep sky blue', 'dim gray', 'dodger blue', 'firebrick1', 
'forest green', 'gainsboro', 'gold', 'goldenrod', 'gray', 'green yellow', 'honeydew2', 'hot pink', 'indian red', 'ivory2', 'khaki', 'lavender', 'lawn green', 
'lemon chiffon', 'light blue', 'light coral', 'light cyan', 'light goldenrod', 'light goldenrod yellow', 'light grey', 'light pink', 'light salmon', 'light sea green', 
'light sky blue', 'light slate blue', 'light slate gray', 'light steel blue', 'light yellow', 'lime green', 'linen', 'magenta2', 'maroon', 'medium aquamarine', 
'medium blue', 'medium orchid', 'medium purple', 'medium sea green', 'medium slate blue', 'medium spring green', 'medium turquoise', 'medium violet red', 'midnight blue', 
'misty rose', 'navajo white', 'navy', 'olive drab', 'orange', 'orange red', 'orchid1', 'pale goldenrod', 'pale green', 'pale turquoise', 'pale violet red', 'papaya whip', 
'peach puff', 'pink', 'pink1', 'plum1', 'powder blue', 'purple', 'red', 'rosy brown', 'royal blue', 'saddle brown', 'salmon', 'sandy brown', 'sea green', 'seashell2', 
'sienna1', 'sky blue', 'slate blue', 'slate gray', 'snow', 'spring green', 'steel blue', 'tan1', 'thistle', 'tomato', 'turquoise', 'violet red', 'wheat1', 'yellow', 'yellow green']
preprocessingDirectives = ('#include', '#if', '#ifdef', '#ifndef', '#else', '#elif', '#endif', '#define', '#undef', '#line', '#error', '#pragma', '...', '__VA_ARGS__','__VA_OPT__')
oneCharOperatorList = ('.','+','-','*','/','%', '&', '|', '<', '>', '!', '^', '~', '?', ':', '=', ',')
twoCharOperatorList = ('##','++', '--','()','[]','->','>>', '<<', '<=', '>=', '==', '!=', '&&', '||', '+=', '-=', '*=', '/=', '%=', '&=', '^=', '|=')
threeCharOperatorList = ('<<=', '>>=')
derivedOperatorList = ("function()","typecast")
bracesDict = 		{	"(":")",	"{":"}",	"[":"]",	"<":">",	"?":":"}
bracesDictReverse = {	")":"(",	"}":"{",	"]":"[",	">":"<",	":":"?"}
primitiveDatatypeLength = {"char":CHAR_SIZE,"short":SHORT_SIZE,"int":INT_SIZE, "long":LONG_SIZE, "long long":LONG_LONG_SIZE,"pointer":POINTER_SIZE, "float":FLOAT_SIZE,"double":DOUBLE_SIZE}

cDataTypes = ["char","double","float","int", "long","short","void","signed","unsigned"]
cKeywords = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", 
				"extern", "float", "for", "goto", "if", "inline", "int", "long", "register", "return", "short", "signed", 
				"sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]
integralDataTypes = ["char","short","int","long","long long"]
treeViewHeadings = ["Variable Name", "Data Type", "Addr Start", "Addr End", "Raw Hex Bytes", "Value (LE)", "Value (BE)"]

PACKED_STRING 		= "__packed__"
ALIGNED_STRING 		= "__aligned__"
ATTRIBUTE_STRING 	= "__attribute__"

illegalVariableNames = list(preprocessingDirectives) + list(oneCharOperatorList) + list(twoCharOperatorList) + list(threeCharOperatorList) + cDataTypes + cKeywords + integralDataTypes

lines = []
defsByLines = [] # This tells which all #defines are defined at any line.
enums = {}		# This is a dictionary that holds yet another dictionary inside {enumDatatype,{enumFields,enumFieldValues}}
enumFieldValues = {}	# This is a dictionary of ALL enum fields and their values. We can do this because enum field names are globally unique. We keep this separate to cache the enum values
typedefs = {}
structuresAndUnionsDictionary = {}	# Each value of this dictionary is a dictionary itself, where the key is its name. The dictionary is of this format: 
							# "type" : "struct/union", "size":size, "components":[[variable1 name, variable size, variable declaration statement, Extended variable description],...]}
# Below is a list of 6-Tuple. Each list item is pretty much same as the structuresAndUnionsDictionary["components"] 5-tuple, plus another item which tells where this var name occurs.
# [variable1 name, variable size, variable declaration statement, variable name relative index within declaration, Extended variable description, absolute Index of variable name in tokenList]							
variableDeclarations = []
# This is just the sizes of the selected variables that would be colored
tokenLocationLinesChars = []
unraveled = []
fileDisplayOffset = 0 	# This is the offset from which the file display window starts
dataLocationOffset = 0	# This is the offset from which the variables under variablesAtGlobalScopeSelected start to map
codeFileName = None
dataFileName = None
dataFileSizeInBytes = None
displayBlock = []	# This is the block that holds the data for the display window only, starting at fileDisplayOffset
dataBlock = []		# This is the block that holds the data for the variablesAtGlobalScopeSelected[], starting at dataLocationOffset
inputIsHexChar = False
binaryArray = ""
hexCharArray = []
totalBytesToReadFromDataFile = 0
window = None
dummyVariableCount = 0
dummyZeroWidthBitfieldVariableCount = 0
totalVariableCount = 0
globalScopes = []	# These are the variables that are at the global scope, depending on the user selection
globalScopesSelected = []	# These are the variables that are at the global scope, depending on the user selection and the MAP_TYPEDEFS_TOO
variableSelectedIndices = [] # These are the indices of variables that have been selected after the user presses the "Map" button
variablesAtGlobalScopeSelected = [] # These are the variables that are at the global scope, AND are the top-level parents of variables that have been selected by the user
sizeOffsets = []	# These tell the beginning offset (absolute, not relative) and length for ALL the variables under variablesAtGlobalScopeSelected[], beginning at dataLocationOffset.
                    # Each row in sizeOffsets is [variableId,beginOffset,variableSize]
inputVariables = []	# For batch, the list of the Global variables the user wants to map
MAINLOOP_STARTED = False
pragmaPackStack = []
pragmaPackCurrentValue = None
pragmaPackDefaultValue = ALIGNED_DEFAULT_VALUE

LARGE_NEGATIVE_NUMBER = -9999999999999999999999999999999		# A number usually associated with default (erroneous) value of Index in an array

# This thing should be moved out since there is no need to repeat this for every tokenizeLines() invocations
keywordsSorted = list(preprocessingDirectives)
keywordsSorted.extend(list(twoCharOperatorList))
keywordsSorted.extend(list(threeCharOperatorList))
keywordsSorted.sort(key=len)
keywordsSorted.reverse()
PRINT("sorted keyword list =",keywordsSorted)


def errorRoutine(message):
	global window, PRINT_DEBUG_MSG
	backedUpValuePRINT_DEBUG_MSG = PRINT_DEBUG_MSG
	PRINT_DEBUG_MSG = True
	PRINT (message)
	if not BATCHMODE and MAINLOOP_STARTED:
		messageBox.showerror("Error",message)
	PRINT_DEBUG_MSG = backedUpValuePRINT_DEBUG_MSG
	return
	
def warningRoutine(message):
	global window
	PRINT (message)
	if not BATCHMODE and MAINLOOP_STARTED:
		messageBox.showwarning("Warning",message)
	return

def printHelp():
	OUTPUT("The way to invoke this tool is the following:\npython2/3 ParseIT.py [options], where the options are:\n")
	OUTPUT("-h, --help                Prints the options available")
	OUTPUT("-i, --include             followed by a single string that contains the include file path(s), separated by semicolon")
	OUTPUT("-x, --hex                 Prints the integral values in Hex (default is Decimal)")
	OUTPUT("-d, --datafile            followed by the data file name")
	OUTPUT("-c, --codefile            followed by the code file name")
	OUTPUT("-o, --offset              followed by the offset value (from which offset in the data file the struct will start mapping from)")
	OUTPUT("                          Offsets can be numbers or expressions, but must be then double-quoted, like \"3KB+0x12*43-(0o62/0b10)\"")
	OUTPUT("-g, --global              followed by the name of the Global-level variables (or typedefs) that will be mapped")
	OUTPUT("                          If providing multiple variable names, then it must be double-quoted (like \"var1 var2\")")
	OUTPUT("                          If no variable names are provided, every variable at the global level in the code file will be automatically selected")
	OUTPUT("-t, --typedef             followed by Yes/No to indicate if typedefs will be mapped as regular variables or not")
	OUTPUT("-v, --verbose, --debug    to indicate if debug messages will be printed or not")
	OUTPUT("-b, --batch               to indicate that the tool will run in the non-interactive, non-GUI, terminal batch mode")
	

def parseCommandLineArguments():
	global BATCHMODE, codeFileName, dataLocationOffset, inputVariables, PRINT_DEBUG_MSG, MAP_TYPEDEFS_TOO, COMPILER_PADDING_ON, STRUCT_END_PADDING_ON, INCLUDE_FILE_PATHS
	PRINT ("sys.argv = ",sys.argv)
	
	DATAFILENAME = None
	CODEFILENAME = None
	DATAOFFSET = None
	VARIABLENAMES = None
	map_typedefs_too_response = None

	TRUE_VALUES  = ("y","yes","t","true","1", "on")
	FALSE_VALUES = ("n","no","f","false","0","off")
	
	for item in sys.argv:
		if item.lower() in ("-h", "--h", "-help", "--help"):
			printHelp()
			sys.exit()
		else:
			continue
			
	N = 1
	while N <= len(sys.argv)-1:
		if sys.argv[N].lower() in ("-b", "--b", "-batch", "--batch"):
			PRINT ("Operating in Batch mode (no GUI)")
			BATCHMODE = True
			N += 1
		elif sys.argv[N].lower() in ("-i", "--i", "-include", "--include"):
			PRINT ("Include file path")
			N += 1
			if N == len(sys.argv) or sys.argv[N].startswith("-"):
				OUTPUT("Must supply a quoted string containing the include file path(s), separated by semicolon if multiple paths are supplied")
				sys.exit()
			else:
				INCLUDE_FILE_PATHS = sys.argv[N]
			N += 1
		elif sys.argv[N].lower() in ("-x", "--x", "-hex", "--hex", "-hexadecimal", "--hexadecimal"):
			PRINT ("Integral values will be printed in Hexadecimal (default is Decimal)")
			DISPLAY_INTEGRAL_VALUES_IN_HEX = True
			N += 1
		elif sys.argv[N].lower() in ("-p", "--p", "-cp", "--cp", "-pad", "--pad"):
			PRINT ("Compiler padding will be turned on")
			COMPILER_PADDING_ON = True
			STRUCT_END_PADDING_ON = True	# Whether to add additional padding at the end of a structure to make to align to a word boundary
			N += 1
			if N <= len(sys.argv)-1:
				if sys.argv[N].lower() in TRUE_VALUES:
					COMPILER_PADDING_ON = True
					STRUCT_END_PADDING_ON = True	# Whether to add additional padding at the end of a structure to make to align to a word boundary
					N += 1
				elif sys.argv[N].lower() in FALSE_VALUES:
					COMPILER_PADDING_ON = False
					STRUCT_END_PADDING_ON = False	# Whether to add additional padding at the end of a structure to make to align to a word boundary
					N += 1
				else:
					continue
		elif sys.argv[N].lower() in ("-d", "--d", "-df", "--df", "-dfile","--dfile", "-datafile","--datafile"):
			N += 1
			if N > len(sys.argv)-1:
				OUTPUT("Must supply the data filename following the %s option"%sys.argv[N-1])
				sys.exit()
			else:
				DATAFILENAME = sys.argv[N]
				N +=1
		elif sys.argv[N].lower() in ("-c", "--c", "-cf", "--cf", "-cfile","--cfile", "-codefile","--codefile"):
			N += 1
			if N > len(sys.argv)-1:
				OUTPUT("Must supply the code filename following the %s option"%sys.argv[N-1])
				sys.exit()
			else:
				PRINT("Found code file")
				CODEFILENAME = sys.argv[N]
				N +=1
		elif sys.argv[N].lower() in ("-o", "--o", "-do", "--do", "-offset", "--offset", "-doffset", "--doffset", "-dataoffset", "--dataoffset", "-datafileoffset", "--datafileoffset" ):
			N += 1
			if N > len(sys.argv)-1:
				OUTPUT("Must supply the data offset following the %s option"%sys.argv[N-1])
				sys.exit()
			else:
				DATAOFFSET = sys.argv[N]
				convertByteUnits2DecimalResult = convertByteUnits2Decimal(DATAOFFSET)
				if convertByteUnits2DecimalResult[0] == False:
					OUTPUT(DATAOFFSET,"is not a valid data offset")
					sys.exit()
				elif not checkIfIntegral(convertByteUnits2DecimalResult[1]):
					OUTPUT("Supplied data offset %s must be an integer"%DATAOFFSET)
					sys.exit()
				elif convertByteUnits2DecimalResult[1] < 0:
					OUTPUT("Supplied data offset %d must be a non-negative integer"%DATAOFFSET)
					sys.exit()
				else:
					dataLocationOffset = convertByteUnits2DecimalResult[1]
				N +=1
		elif sys.argv[N].lower() in ("-g", "--g") or sys.argv[N].lower().startswith("-global") or sys.argv[N].lower().startswith("--global") :
			N += 1
			if N > len(sys.argv)-1:
				OUTPUT("Must supply the global variable name(double-quoted list if multiple) following the %s option"%sys.argv[N-1])
				sys.exit()
			else:
				VARIABLENAMES = sys.argv[N]
				N +=1
		elif sys.argv[N].lower() in ("-debug","--debug","-v","--v","-verbose","--verbose"):
			N += 1
			if N > len(sys.argv)-1:
				OUTPUT("Turning Debug ON")
				PRINT_DEBUG_MSG = True
				N += 1
			else:
				if sys.argv[N].startswith("-"):
					OUTPUT("Turning Debug ON")
					PRINT_DEBUG_MSG = True
				else:
					print_debug_msg_Response = sys.argv[N]
					if print_debug_msg_Response.lower() in TRUE_VALUES:
						PRINT_DEBUG_MSG = True
						N +=1
					elif print_debug_msg_Response.lower() in FALSE_VALUES:
						PRINT_DEBUG_MSG = False
						N += 1
					elif N==len(sys.argv)-1 and DATAFILENAME==None:
						pass
					else:
						OUTPUT("Unknown value for Debug option")
						sys.exit()
		elif sys.argv[N].lower() in ("-t", "--t", "-td", "--td", "-typedef", "--typedef", "-typedefs", "--typedefs", "-mt", "--mt", "-map_typedefs", "--map_typedefs" ):
			N += 1
			if N > len(sys.argv)-1:
				OUTPUT("Must tell whether to map typedefs too or not, following the %s option"%sys.argv[N-1])
				sys.exit()
			else:
				map_typedefs_too_response = sys.argv[N]
				if map_typedefs_too_response.lower() in FALSE_VALUES:
					PRINT ("NOT mapping the typedefs")
					MAP_TYPEDEFS_TOO = False
				elif map_typedefs_too_response.lower() in TRUE_VALUES:
					PRINT ("Mapping the typedefs too")
					MAP_TYPEDEFS_TOO = True
				else:
					OUTPUT("Must tell whether to map typedefs too or not, following the %s option - %s is not a valid response"%(sys.argv[N-1]),map_typedefs_too_response)
					sys.exit()
				N +=1
		else:
			PRINT ("N = ",N,"len(sys.argv)-1 =",len(sys.argv)-1)
			if DATAFILENAME == None and N == len(sys.argv)-1:
				DATAFILENAME = sys.argv[N]
				N += 1
			else:
				OUTPUT("Unknown parameter %s supplied - exiting"%sys.argv[N])
				printHelp()
				sys.exit()

	if CODEFILENAME == None:
		if BATCHMODE:
			OUTPUT("Must supply code file")
			printHelp()
			sys.exit()
	else:
		PRINT ("Chosen Code file name = ",CODEFILENAME)
		codeFileName = CODEFILENAME
				
	if DATAFILENAME == None:
		if BATCHMODE:
			OUTPUT("Must supply data file")
			printHelp()
			sys.exit()
	else:
		PRINT ("Chosen Data file name = ",DATAFILENAME)
		# This will automatically populate the dataFileName, dataFileSizeInBytes, and inputIsHexChar
		if not openDataFileRoutineBatch(DATAFILENAME):
			OUTPUT ("Error opening",DATAFILENAME)
			sys.exit()
		
		
	if DATAOFFSET != None:
		if BATCHMODE:
			PRINT ("Input Data Offset = ",DATAOFFSET,"results in",dataLocationOffset)
			if dataLocationOffset >= dataFileSizeInBytes:
				OUTPUT("Input Data Offset = ",DATAOFFSET,"(",dataLocationOffset,") too big for data file of size",dataFileSizeInBytes)
				sys.exit()
			
	if BATCHMODE and VARIABLENAMES != None:
		PRINT ("Chosen top-level variable name(s) = ",VARIABLENAMES)
		inputVariables = re.sub("[,\s]+"," ",VARIABLENAMES.strip()).split(" ")
	

	return True


	
class Node (object):
	def __init__ (self, data, type):
		self.data = data
		self.type = type
		self.children = []
		
	def add_child (self, obj):
		self.children.append(obj)
	
	# Preorder traversal of a N-ary tree
	def traverse (self,level=0):
		PRINT (" "+"--"*level,level," type = <",self.type, ">, ", len(self.children), " children, data = <",self.data, ">" )
		if len(self.children) > 0:
			for i in self.children:
#				PRINT ("Going to traverse the children of ", self )
				i.traverse(level+1)
	
	def populateStructuresAndUnionsDictionary(self, structOrUnionName):
		if self.type != "struct" and self.type != "union" :
			return
		
# This function takes in an input List, and returns the sum of the elements (assumed to be integers)
def listItemsSum(inputList):
	if not isinstance(inputList,list):
		PRINT ("ERROR: Illegal input array dimension value",arrayDimensions )
		return False
	elif len(inputList) == 0:	# Blank
		return False
	elif inputList:
		returnValue = 0
		for item in inputList:
			if not isinstance(item, int):
				return False
			else:
				if item <= 0:
					PRINT ("WARNING: non-positive integer",item )
				returnValue += item
		return returnValue
	else:
		PRINT ("ERROR!!!!" )
		sys.exit()

# This function takes in an input List, and returns the product of the elements (assumed to be integers)
def listItemsProduct(inputList):
	if not isinstance(inputList,list):
		PRINT ("ERROR: Illegal input array dimension value",arrayDimensions )
		return False
	elif len(inputList) == 0:	# Blank
		return False
	elif inputList:
		returnValue = 1
		for item in inputList:
			if not isinstance(item, int):
				return False
			else:
				if item <= 0:
					PRINT ("WARNING: non-positive integer",item )
				returnValue *= item
		return returnValue
	else:
		PRINT ("ERROR!!!!" )
		sys.exit()

########################################################################################################################################################################
# This function returns the Array Indices for an array element position. For example, if there is an array[Di][Dj][Dk], where Di/Dj/Dk are array dimensions, then we can
# potentially have (Di x Dj x Dk) number of array elements, starting from 0 to (Di x Dj x Dk - 1). So, given inputs of Di, Dj, Dk (the array dimensions) and 
# the array element position (a number between 0 and (Di x Dj x Dk - 1)), this routine outputs [i,j,k] such that essentially in C language, *(array + position) = array[i][j][k]
########################################################################################################################################################################
def calculateArrayIndicesFromPosition(arrayDimensions, position):
	
#	PRINT ("inside calculateArrayIndices(arrayDimensions=",arrayDimensions, "position=",position,")" )
	if not isinstance(arrayDimensions,list):
		PRINT ("ERROR: Illegal input array dimension value",arrayDimensions )
		return False
	elif (not isinstance(position,int)) or (position < 0):	
		PRINT ("ERROR: Illegal input array position value",position )
		return False
	else:
		totalCount = 1
		cumulativeProduct = 1
		arrayDimensionsReversed = arrayDimensions[::-1]
		reverseIndex = []
		for i in range(len(arrayDimensionsReversed)):
			d = arrayDimensionsReversed[i]
			if (not isinstance (d, int)) or (d <1):
				PRINT ("ERROR: Illegal input array dimension value",d )
				return False
			else:
				totalCount *= d
				if i==0:
					cumulativeProduct = 1
		
				reverseIndex.append(cumulativeProduct)
				cumulativeProduct *= d
				
		if position >= totalCount:
			PRINT ("ERROR: Illegal input array position value", position," - it cannot be bigger than", totalCount-1, "for array dimensions",arrayDimensions )
			return False
	
		arrayDimensionSizes = reverseIndex[::-1]
		
#		PRINT ("For arrayDimensions =",arrayDimensions,"arrayDimensionSizes=",arrayDimensionSizes )
		
		temp = position
		arrayIndices = []
		for i in range(len(arrayDimensionSizes)):
			arrayIndices.append(integerDivision(temp,arrayDimensionSizes[i]))
			temp = temp%arrayDimensionSizes[i]
#		PRINT ("For arrayDimensions =",arrayDimensions,"position=",position,"arrayIndices =",arrayIndices )

		if position != calculateArrayPositionFromIndices(arrayDimensions, arrayIndices):
			PRINT ("ERROR!!!For arrayDimensions =",arrayDimensions,"position=",position,"calculated arrayIndices =",arrayIndices,"does not match" )
			return False
		else:
			return arrayIndices
		
########################################################################################################################################################################
# This function returns the position of an array element from an input of Array dimensions and Array Indices. For example, if there is an array[Di][Dj][Dk], 
# where Di/Dj/Dk are array dimensions, then we can potentially have (Di x Dj x Dk) number of array elements, starting from 0 to (Di x Dj x Dk - 1). 
# So, given inputs of Di, Dj, Dk (the array dimensions) and Array indices [i,j,k], it returns the array element position - a number between 0 and (Di x Dj x Dk - 1)
# this routine outputs position such that essentially in C language, *(array + position) = array[i][j][k]
########################################################################################################################################################################
def calculateArrayPositionFromIndices(arrayDimensions, arrayIndices):
	
#	PRINT ("inside calculateArrayPositionFromIndices(arrayDimensions=",arrayDimensions, "arrayIndices=",arrayIndices,")" )
	if (not isinstance(arrayDimensions,list)) or (not isinstance(arrayIndices,list)):
		PRINT ("ERROR: Illegal value for input array dimension (",arrayDimensions,") or index (",arrayIndices,")" )
		return False
	elif len(arrayDimensions) != len(arrayIndices):
		PRINT ("ERROR: Length of input array dimension (",arrayDimensions,") does not match length of array index length(",arrayIndices,")" )
		return False
	else:
		for i in range(len(arrayDimensions)):
			if not isinstance(arrayDimensions[i], int):
				PRINT ("ERROR: non-integral array dimension (",arrayDimensions,") " )
				return False
			elif arrayDimensions[i] <1:
				PRINT ("ERROR: array dimension size must at least be 1 - arrayDimensions[",i,"] =",arrayDimensions[i] )
				return False
		for i in range(len(arrayIndices)):
			if not isinstance(arrayIndices[i], int):
				PRINT ("ERROR: non-integral array index (",arrayIndices,") " )
				return False
			elif arrayIndices[i] <0:
				PRINT ("ERROR: array index must at least be 0 - currently, arrayIndices[",i,"] =",arrayIndices[i] )
				return False
			elif arrayIndices[i] >= arrayDimensions[i]:
				PRINT ("ERROR: array index ", arrayIndices[i]," cannot be numerically equal or bigger than its dimension size (",arrayDimensions[i],") " )
				return False
				
		cumulativeProduct = 1
		arrayDimensionsReversed = arrayDimensions[::-1]
		reverseIndex = []
		for i in range(len(arrayDimensionsReversed)):
			if i==0:
				cumulativeProduct = 1
			reverseIndex.append(cumulativeProduct)
			cumulativeProduct *= arrayDimensionsReversed[i]
			
		arrayDimensionSizes = reverseIndex[::-1]
		
#		PRINT ("For arrayDimensions =",arrayDimensions,"arrayDimensionSizes=",arrayDimensionSizes )
		
		position = 0
		for i in range(len(arrayDimensionSizes)):
			position += arrayIndices[i]*arrayDimensionSizes[i]
#		PRINT ("For arrayDimensions =",arrayDimensions," and arrayIndices=", arrayIndices,"position=",position )
		return position
		
		

#######################################################################################################################################################
# This prints the input lines, numbered and delimited by <>. Like Line # 0. <....> etc.
#######################################################################################################################################################
def printLines(lines):
	# Check that lines is a list of Lines (strings ending with a newline). If it is a single string, make it a list
	if  isinstance(lines,list):
		itemCount = 0
		while itemCount < len(lines):
			if not checkIfString(lines[itemCount]):
				PRINT ("lines is not a list of proper strings - ", lines )
				return False
				sys.exit()
			itemCount = itemCount + 1
		itemCount = 0
		while itemCount < len(lines):
			PRINT ("Line # %2d = <%s>"%(itemCount,lines[itemCount]) )
			itemCount = itemCount + 1
	else:
		if checkIfString(lines):
			PRINT ("Line #  0 = <%s>"%lines )
		else:
			PRINT ("Unknown object type - lines = <",lines,"> - exiting" )
			return False
			sys.exit()
			
	return True

#######################################################################################################################################################
# This function taken in a List, and progressively removes listification until we get a list with at least 2 members.
# For example, it will reduce the list [[[['a','+','b']]]] to ['a','+','b'].
# The reason we have this function is because sometimes we want to compare two lists, and even if they are not the same from the programmatic
# point of view, they are essentially the same.
#######################################################################################################################################################
def removeUnnecessaryListification(inputList):
	if isinstance(inputList,list):
		if len(inputList) == 1 and isinstance(inputList[0],list):
			return removeUnnecessaryListification(inputList[0])
		else:
			return inputList
	else:
		return inputList
	
#######################################################################################################################################################
# This function taken a string consisting of filepaths separated by semicolon, and returns a list of such filepaths.
# For example, if you call it for "C:/Windows/Users; C:/Temp", it will return ["C:/Windows/Users/", "C:/Temp/"]
# Each of the returned list item will have the proper () slash at the end, and no semicolon.
#######################################################################################################################################################
def returnFilePathList(semicolonSeparatedFilePaths):
	if not checkIfString(semicolonSeparatedFilePaths):
		errorMessage = "ERROR in returnFilePathList- supplied input semicolonSeparatedFilePaths = <%s> is not a string"%(STR(semicolonSeparatedFilePaths))
		errorRoutine(errorMessage)
		return False
	if semicolonSeparatedFilePaths.strip() == "":
		return []
	# Get the current working directory
	cwd = os.getcwd()
	scriptLocation = os.path.realpath(__file__)
	if "\\" in cwd and "/" in cwd and "\\" in scriptLocation and "/" in scriptLocation:
		errorMessage = "ERROR in returnFilePathList() - both current working directory path and script location contain both forward slash and backward slash - cannot figure out if Unix or Windows"
		errorRoutine(errorMessage)
		return False
	
	dirToCheck = scriptLocation if "\\" in cwd and "/" in cwd else cwd
	
	if "\\" in dirToCheck:
		PRINT("Window-based system, where file path is punctuated by backward slash")
		slashType = "\\"
		slashTypeOpposite = "/"
	elif "/" in dirToCheck:
		PRINT("Unix-based system, where file path is punctuated by forward slash")
		slashType = "/"
		slashTypeOpposite = "\\"
	else:
		OUTPUT("Coding error in returnFilePathList() - exiting")
		sys.exit()
	
	if ';' in semicolonSeparatedFilePaths:
		temp = semicolonSeparatedFilePaths.strip().split(';')
	else:
		temp = [semicolonSeparatedFilePaths.strip()]
		
	PRINT("semicolonSeparatedFilePaths = <%s>"%semicolonSeparatedFilePaths)
	PRINT("paths = ",temp)
	
	
	paths = []
	for i in range(len(temp)):
		PRINT("Currently handling path = <%s> for path index %d"%(temp[i],i))
		temp[i] = temp[i].strip()
		PRINT("Currently handling path = <%s> for path index %d (after trimming)"%(temp[i],i))
		if not temp[i]:
			pass
		else:
			temp[i] = temp[i].replace(slashTypeOpposite, slashType)
			if temp[i][-1] != slashType:
				temp[i] += slashType
			paths.append(temp[i])
			
	PRINT("Returning paths =",paths)
	return paths
	
#returnFilePathList(";c:/Windows/Users; ; c:\\temp\\;;")
#sys.exit()

#######################################################################################################################################################
# This function takes an input list, and returns True/False based upon whether the input List is a valid Abstract Syntax Tree or not
#######################################################################################################################################################
def isASTvalid(inputList):
	global cDataTypes;
	
	validOperators = oneCharOperatorList+twoCharOperatorList+threeCharOperatorList+derivedOperatorList
	validPrefixOperators = ["++","--","+","-","!","~","*","&","sizeof","_Alignof","()","{}","[]",",","function()","typecast"]
	validPostfixOperators = ["++","--"]
	validInfixOperators = [".","->","*","/","%","+","-",">>","<<","<","<=",">",">=","==","!=","&","^","|","&&","||","=","+=","-=","*=","/=","%=","<<=",">>=","&=","^=","|=",","]
	
	if checkIfString(inputList):
		return True
	elif isinstance(inputList,list):
		if len(inputList) == 0:
			return True
		elif len(inputList) == 1:
			return True
		elif len(inputList) == 2:
			# Check the prefix ones of the format [prefix-operator, operand]
			if (inputList[0] in validPrefixOperators) and (inputList[1] not in validOperators):
				return isASTvalid(inputList[1])
			elif (inputList[0] not in validOperators) and (inputList[1] in validPrefixOperators):
				return isASTvalid(inputList[0])
			elif (inputList[0] == 'datatype'): 
				for item in inputList[1]:
					if item not in cDataTypes:
						PRINT ("item", item,"in inputList[1] = ",inputList[1], "doesn't belong to either primitiveDatatypeLength.keys() =",getDictKeyList(primitiveDatatypeLength), "or typedefs.keys() = ",getDictKeyList(typedefs) )
						return False
				return True
			else:
				PRINT ("inputList =",inputList, "is not a valid 2-element AST" )
				return False
		elif len(inputList) == 3:
			if inputList[0] == "function()": 
				if inputList[1] not in validOperators:
					# TO-DO - put a check that a function name must be a valid string and not a list (but beware of macro)
					return isASTvalid(inputList[2])
				else:
					return False
			elif (inputList[0] not in validOperators) and (inputList[1] in validInfixOperators) and (inputList[2] not in validOperators):
				return isASTvalid(inputList[0]) & isASTvalid(inputList[2])
			else:
				PRINT ("inputList =",inputList, "is not a valid AST" )
				return False
		elif len(inputList) == 5: # Ternary operator
			if (inputList[0] not in validOperators) and (inputList[1]=="?") and (inputList[2] not in validOperators) and (inputList[3]==":") and (inputList[4] not in validOperators):
				PRINT ("inputList[0] =",inputList[0],"inputList[2] =",inputList[2],"inputList[4] =",inputList[4], )
				return isASTvalid(inputList[0]) & isASTvalid(inputList[2]) & isASTvalid(inputList[4])
		else:
			PRINT ("inputList =",inputList, "is not a valid AST" )
			return False


#######################################################################################################################################################
# This function takes an input list, and returns a deep copy of the list
#######################################################################################################################################################
def listDeepCopy(inputList):
	if checkIfString(inputList):
		returnString = '%s'%inputList	# Not really necessary since Strings are immutable anyway, still if we really insist on creating a separate copy ....
		return returnString
	elif isinstance(inputList,list):
		returnList = []
		i = 0
		while i < len(inputList):
			returnList.append(listDeepCopy(inputList[i]))
			i = i+1
		return returnList
	else:
		return inputList

##############################################################################################################################################################
# When we are supplying a string to a regular expression module, the string may contain characters that are used for regular expressions, like *, \, ( + etc.
##############################################################################################################################################################
def escapeREmetacharacters(inputString):
	if not checkIfString(inputString):
		PRINT ("inputString =",inputString,"is not a string - exiting!" )
		return False
		sys.exit()
	else:
		outputString = ''
		reMetacharacters = ['*','+','\\','[',']','(',')','.','^','$','{','}','|','?']
		for c in inputString:
			outputString = outputString + ('\\' + c if c in reMetacharacters else c)
		return outputString
		
#######################################################################################################################################################
# This function returns the size of the datatype.
#
# This function will NOT be able to return the correct value for very complicated expressions, because unlike a full-ledged compiler, here we are
# NOT actually allocating any memory on the stack. Hence, it cannot handle complex expressions involving * and &.
#
# It can only handle very simple expressions like sizeof(S1.S2.S3.i) etc.
#
#######################################################################################################################################################
def getDatatypeSize(inputList):
	PRINT ("\n\n","=="*50,"\nGoing to evaluate getDatatypeSize(inputList) for inputList =",inputList)
	if isinstance(inputList,list):
		if len(inputList) == 1:
			return getDatatypeSize(inputList[0])
		elif len(inputList) == 2 and inputList[0] in ("struct","union"):
			return getDatatypeSize(inputList[1])
		elif len(inputList) == 2 and inputList[0] in ("datatype"):
			return getDatatypeSize(inputList[1])
		elif len(inputList)>1 and inputList[-1] == "*":	# This is handling cases like "unsigned char *"
			allItemsAreDatatypes = True
			for item in inputList[:len(inputList)-1]:
				if ((item not in getDictKeyList(primitiveDatatypeLength)) and 
				    (item not in getDictKeyList(cDataTypes)) and 
				    (item not in getDictKeyList(typedefs)) and 
					(item not in getDictKeyList(structuresAndUnionsDictionary))):
					allItemsAreDatatypes = False
					break
			if allItemsAreDatatypes:
				return primitiveDatatypeLength["pointer"]
			else:
				errorMessage = "ERROR: unknown items prior to pointer in <%s>  - exiting"%(STR(inputList))
				errorRoutine(errorMessage)
				return False
		elif len(inputList) == 3 and inputList[1] in (".","->"):
			PRINT("variableDeclarations =")
			for item in variableDeclarations: PRINT(item)
			PRINT("structuresAndUnionsDictionary =")
			for key,value in structuresAndUnionsDictionary.items() : PRINT("key =",key,"value =",value)
			PRINT("Struct member operator")
			flattenedList = flattenList(inputList)
			PRINT ("Will try to make sense of the following expressions:",flattenedList)
			newSize = -1
			N = 0
			while N < len(flattenedList):
				PRINT ("\n"*2,"N =",N,"\n"*2)
				gotoNextCycle = False
				if N==0:
					# For the first item, it must be a declared variable (so check in variableDeclarations)
					nextDataType = ""
					for item in variableDeclarations:
						if item[0] == flattenedList[N]:
							PRINT ("variable",item[0],"exists in variableDeclarations")
							variableDescription = item[4]
							PRINT ("For variable",item[0],", variable description = ",variableDescription)
							datatype = variableDescription["datatype"]
							PRINT ("variable",item[0],"\'s datatype = ",datatype)
							if datatype in getDictKeyList(structuresAndUnionsDictionary):
								PRINT ("variable",item[0],"\'s datatype = ",datatype,"is a struct/union")
								components = structuresAndUnionsDictionary[datatype]["components"]
								for c in components:
									if c[0] == flattenedList[N+2]:
										nextDataType = c[4]["datatype"]
										newSize = c[1]
										break
							else:
								errorMessage = "ERROR: cannot use %s operator on non-member variable %s - exiting"%(STR(flattenedList[N+1]), STR(flattenedList[N+2]))
								errorRoutine(errorMessage)
								return False
							PRINT ("For new variable",flattenedList[N+2],", datatype = ",nextDataType,", size =",newSize)
					if nextDataType == "":
						errorMessage = "ERROR: cannot use %s operator on non-member variable %s - exiting"%(STR(flattenedList[N+1]), STR(flattenedList[N+2]))
						errorRoutine(errorMessage)
						return False
					else:
						N = N + 2
						gotoNextCycle = True
						continue
				elif N == len(flattenedList)-1:
					return newSize
				elif N < len(flattenedList)-1 and flattenedList[N+1] in (".","->") and nextDataType not in getDictKeyList(structuresAndUnionsDictionary):
						errorMessage = "ERROR: cannot use %s operator on non-struct variable %s - exiting"%(STR(flattenedList[N+1]), STR(flattenedList[N]))
						errorRoutine(errorMessage)
						return False
				elif N < len(flattenedList)-1 and flattenedList[N+1] in (".","->") and (N+1==len(flattenedList)-1):
					errorMessage = "ERROR: cannot use %s operator on struct variable %s without specifying any member variable - exiting"%(STR(flattenedList[N+1]), STR(flattenedList[N]))
					errorRoutine(errorMessage)
					return False
				elif ("components" not in getDictKeyList(structuresAndUnionsDictionary[nextDataType])) or (structuresAndUnionsDictionary[nextDataType]["components"] =={}):
					PRINT (getDictKeyList(structuresAndUnionsDictionary[nextDataType]))
					errorMessage = "ERROR: cannot use %s operator on blank struct variable %s - exiting"%(STR(flattenedList[N+1]), STR(nextDataType))
					errorRoutine(errorMessage)
					return False
				else:
					PRINT ("Passed error checks for N=",N,"nextDataType =",nextDataType)
					components = structuresAndUnionsDictionary[nextDataType]["components"]
					componentFound = False
					for c in components:
						if c[0] == flattenedList[N+2]:
							newDataType = c[4]["datatype"]
							newSize = c[1]
							componentFound = True
							PRINT ("For new variable",flattenedList[N+2],", datatype = ",newDataType,", size =",newSize)
							break
					if componentFound == False:
						errorMessage = "ERROR: cannot use %s operator on blank struct variable %s - exiting"%(STR(flattenedList[N+1]), STR(nextDataType))
						errorRoutine(errorMessage)
						return False
					else:
						nextDataType = newDataType
						
						N = N + 2
						gotoNextCycle = True
						
						continue

				if gotoNextCycle == False:
					PRINT("ERROR: The control should never come here - should error out much before")
					errorMessage = "ERROR: The control should never come here - should error out much before. N=%d"%(N)
					errorRoutine(errorMessage)
					return False
				
			if newSize < 0:
				errorMessage = "ERROR: Could not calculate the size"
				errorRoutine(errorMessage)
				return False
			else:
				return newSize
				
		else:
			errorMessage = "ERROR: unknown length list inputList=<%s>  - exiting"%(STR(inputList))
			errorRoutine(errorMessage)
			return False
			
	elif checkIfString(inputList):
#		PRINT ("inputList = <",inputList,"> is a string, now checking")
		if inputList in getDictKeyList(primitiveDatatypeLength):
			return primitiveDatatypeLength[inputList]
		elif inputList in getDictKeyList(structuresAndUnionsDictionary):
			return structuresAndUnionsDictionary[inputList]["size"]
		elif inputList in getDictKeyList(typedefs):
#			return getDatatypeSize(typedefs[inputList])		#Bug fix on 2020-03-04
			return typedefs[inputList][1]
		else:
			PRINT ("Checking if ",inputList,"is any of the variables declared before" )
			PRINT (variableDeclarations )
			for i in range(len(variableDeclarations)):
				if variableDeclarations[i][0] == inputList:
					return variableDeclarations[i][1]
			PRINT ("The variable",inputList,"is any of the variables declared before, hence cannot determine the size of" )
			errorMessage = "ERROR: The variable"+inputList+"is any of the variables declared before, hence cannot determine the size of"
			errorRoutine(errorMessage)
			return False
	else:
		errorMessage = "ERROR: Unknown inputList <%s>  - exiting"%(STR(inputList))
		errorRoutine(errorMessage)
		return False
		
	
def isStringAValidNumber(numericString):
	if numericString.isdigit():
#		PRINT ("Is digit")
		return True
	elif checkIfString(numericString):
		PRINT ("numericString =",numericString,"is string")
		if "." in numericString: 
#			PRINT ("has a decimal point")
			if numericString.count(".")>1:
#				PRINT ("more than once")
				return False
			else:
#				PRINT ("only once")
				if numericString[-1] == ".":
					PRINT ("The decimal cannot be at the end") 
					return False
				elif numericString[0] == ".":
					return numericString[1:].isdigit()
				else:
					digitParts = re.split(r"\.",numericString)
#					PRINT ("digitParts =",digitParts)
					if len(digitParts) != 2:
						return False
					else:
						return digitParts[0].isdigit() and digitParts[1].isdigit()
		else:
			return False
	else:
		return False


#######################################################################################################################################################
#
# 						!!!! 	THIS FUNCTION NEEDS AN AST, NOT JUST A LIST !!!!!
#
# This function takes a list of tokens representing an Arithmetic Expression AST, evaluates it, and returns the result.
# The input must be a valid AST, otherwise it will not work. Just giving it in the token list form is not sufficient.
# The output from this is a Tuple of a boolean value and a result [True/Flase, result]. The reason we do this is because an arithmetic expression result
# can itself return False as a proper output, so we do not know if that is a true result, or something went wrong.
#######################################################################################################################################################
def evaluateArithmeticExpression(inputAST):
	inputList = inputAST	# Just to remind that the inputList must be an AST
#	PRINT ("For evaluateArithmeticExpression, inputList =", inputList )
	if checkIfString(inputList):
#		PRINT ("It's a string - returning as it is!" )
		if isStringAValidNumber(inputList):
			if '.' in inputList:
				return [True,float(inputList)]
			else:
				return [True, int(inputList)]
		elif len(inputList)>=3 and inputList[:2]=="0x": 
			if re.match("^[a-fA-F0-9]+$",inputList[2:]):
				return[True,int(inputList,16)]
			else:
				errorMessage = "WARNING - non-numeric string <%s> - cannot evaluate HEX undefined constant"%(STR(inputList))
				errorRoutine(errorMessage)
				return [False, None]
		elif len(inputList)>=3 and inputList[:2]=="0o": 
			if re.match("^[0-7]+$",inputList[2:]):
				return[True,int(inputList,8)]
			else:
				errorMessage = "WARNING - non-numeric string <%s> - cannot evaluate Octal undefined constant"%(STR(inputList))
				errorRoutine(errorMessage)
				return [False, None]
		elif len(inputList)>=3 and inputList[:2]=="0b": 
			if re.match("^[01]+$",inputList[2:]):
				return[True,int(inputList,2)]
			else:
				errorMessage = "WARNING - non-numeric string <%s> - cannot evaluate Binary undefined constant"%(STR(inputList))
				errorRoutine(errorMessage)
				return [False, None]
		elif inputList in getDictKeyList(enumFieldValues):
			return [True, int(enumFieldValues[inputList])]
		else:
			errorMessage = "WARNING - non-numeric string <%s> - cannot evaluate undefined constant"%(STR(inputList))
			errorRoutine(errorMessage)
			return [False, None]

	elif isinstance(inputList,list):
	
		if not isASTvalid(inputList):
			warningRoutine("WARNING - evaluating the arithmetic expression may not work because the inputList <" +STR(inputList)+ "> is not a valid AST" )
		
		# If it is a list of lists, but contains only a single member, remove one level of listification
		if len(inputList) == 1:
#			PRINT ("Returning",inputList[0] )
			return evaluateArithmeticExpression(inputList[0])
			
		# 2-member lists
		elif len(inputList) == 2:

			if inputList[0] in ['()','~','+','-',"!","*","&","++"]:
			
				evaluateArithmeticExpressionOutput1 = evaluateArithmeticExpression(inputList[1])
				
				if len(evaluateArithmeticExpressionOutput1) != 2 or evaluateArithmeticExpressionOutput1[0] != True:
					return [False, None]
				else:
					op1 = evaluateArithmeticExpressionOutput1[1]
					
				if   inputList[0] == '()':	# Just parenthesized expression
					result = op1
				elif inputList[0] == '~':
					result = ~op1
				elif inputList[0] == '+':
					result = +op1
				elif inputList[0] == '-':
					result = -op1
				elif inputList[0] == "!":
					if op1 == 0:
						result = 1
					else:
						result = 0
				elif op1 == "*":
					errorMessage = "Operator <"+inputList[0]+"> (Dereferencing) not yet supported (coming soon)"
					errorRoutine(errorMessage)
					return [False, None]
				elif op1 == "&":
					errorMessage = "Operator <"+inputList[0]+"> (Referencing) not yet supported (coming soon)"
					errorRoutine(errorMessage)
					return [False, None]
				elif inputList[0] == "++":
					result = op1 + 1
				else:
					errorMessage = "Operation <"+inputList[0]+"> either not supported or coded"
					errorRoutine(errorMessage)
					return [False, None]
					
			elif inputList[1] == "++":	# TO-DO: Not sure if the interpreter needs to do anything here
				evaluateArithmeticExpressionOutput0 = evaluateArithmeticExpression(inputList[0])
				if len(evaluateArithmeticExpressionOutput0) != 2 or evaluateArithmeticExpressionOutput0[0] != True:
					return [False, None]
				else:
					result = evaluateArithmeticExpressionOutput0[1]
					
			elif inputList[0] == "sizeof":	# TO-DO: Not sure if the interpreter needs to do anything here
				PRINT ("Inside sizeof()" )
				if isinstance(inputList[1],list):
					if len(inputList[1])==2 and inputList[1][0]=="()":
						sizeofType = inputList[1][1]
						PRINT ("Inside sizeof() - calling getDatatypeSize(sizeofType=",sizeofType,")" )
						getDatatypeSizeResult = getDatatypeSize(sizeofType)
						if getDatatypeSizeResult == False or getDatatypeSizeResult == None:
							errorMessage = "ERROR: Finding sizeof(%s)"%(STR(sizeofType))
							errorRoutine(errorMessage)
							return [False, None]
						else:
							PRINT ("Inside sizeof() - return value for getDatatypeSize(sizeofType=",sizeofType,") =",getDatatypeSizeResult )
							return [True, getDatatypeSizeResult]
							
				elif checkIfString(inputList[1]):
					getDatatypeSizeResult = getDatatypeSize(inputList[1])
					if getDatatypeSizeResult == False:
						errorMessage = "ERROR: Finding sizeof(%s)"%(STR(inputList[1]))
						errorRoutine(errorMessage)
						return [False, None]
					else:
						return [True, getDatatypeSizeResult]
				else:
					errorMessage = "ERROR: unknown argument for sizeof(%s) - expected a list "%(STR(inputList[1]))
					errorRoutine(errorMessage)
					return [False, None]
			else:
				errorMessage = "Cannot evaluate Unknown 2-member expression:<%s>"%STR(inputList)
				errorRoutine(errorMessage)
				return [False, None]
				
		# 3-member lists
		elif len(inputList) == 3:

			if inputList[1] in ['+','-','*','/','%','<<','>>','|','&','^','<','>','<=','>=','||','&&','==','!=']:
			
				evaluateArithmeticExpressionOutput0 = evaluateArithmeticExpression(inputList[0])
				if len(evaluateArithmeticExpressionOutput0) != 2 or evaluateArithmeticExpressionOutput0[0] != True:
					PRINT ("ERROR: evaluateArithmeticExpression(inputList[0]) = evaluateArithmeticExpression(",inputList[0],") =",evaluateArithmeticExpressionOutput0 )
					return [False, None]
					
				evaluateArithmeticExpressionOutput2 = evaluateArithmeticExpression(inputList[2])
				if len(evaluateArithmeticExpressionOutput2) != 2 or evaluateArithmeticExpressionOutput2[0] != True:
					PRINT ("ERROR: evaluateArithmeticExpression(inputList[2]) = evaluateArithmeticExpression(",inputList[2],") =",evaluateArithmeticExpressionOutput2 )
					return [False, None]

				op0 = evaluateArithmeticExpressionOutput0[1]
				op2 = evaluateArithmeticExpressionOutput2[1]
			
				# Arithmetic operations
				if   inputList[1] == '+':
					result =  op0 + op2
				elif inputList[1] == '-':
					result =  op0 - op2
				elif inputList[1] == '*':
					result =  op0 * op2
				elif inputList[1] == '/':
					if isinstance(op0,int) and isinstance(op2,int):
						result = integerDivision(op0, op2)
					else:
						result =  op0 / op2
				elif inputList[1] == '%':
					result =  op0 % op2
				elif inputList[1] == '<<':
					result =  op0 << op2
				elif inputList[1] == '>>':
					result =  op0 >> op2
				elif inputList[1] == '|':
					result =  op0 | op2
				elif inputList[1] == '&':
					result =  op0 & op2
				elif inputList[1] == '^':
					result =  op0 ^ op2
					
				# Logical operations
				elif inputList[1] == '<':
					if op0 < op2:
						result = 1
					else:
						result = 0
				elif inputList[1] == '>':
					if op0 > op2:
						result = 1
					else:
						result = 0
				elif inputList[1] == '<=':
					if op0 <= op2:
						result = 1
					else:
						result = 0
				elif inputList[1] == '>=':
					if op0 >= op2:
						result = 1
					else:
						result = 0
				elif inputList[1] == '||':
					if op0 or op2:
						result = 1
					else:
						result = 0
				elif inputList[1] == '&&':
					if op0 and op2:
						result = 1
					else:
						result = 0
				elif inputList[1] == '==':
					if op0 == op2:
						result = 1
					else:
						result = 0
				elif inputList[1] == '!=':
					if op0 != op2:
						result = 1
					else:
						result = 0
			else:
				errorMessage = "Cannot evaluate Unknown 3-member expression:<%s>"%STR(inputList)
				errorRoutine(errorMessage)
				return [False, None]
				
		#Ternary operator
		elif len(inputList) == 5: 
			PRINT ("5-item list" )
			
			if inputList[1] == "?" and inputList[3] == ":":
			
				evaluateArithmeticExpressionOutput0 = evaluateArithmeticExpression(inputList[0])
				if len(evaluateArithmeticExpressionOutput0) != 2 or evaluateArithmeticExpressionOutput0[0] != True:
					return [False, None]
					
				evaluateArithmeticExpressionOutput2 = evaluateArithmeticExpression(inputList[2])
				if len(evaluateArithmeticExpressionOutput2) != 2 or evaluateArithmeticExpressionOutput2[0] != True:
					return [False, None]

				evaluateArithmeticExpressionOutput4 = evaluateArithmeticExpression(inputList[4])
				if len(evaluateArithmeticExpressionOutput4) != 2 or evaluateArithmeticExpressionOutput4[0] != True:
					return [False, None]
			
				if evaluateArithmeticExpressionOutput0[1] == True:
					result = evaluateArithmeticExpressionOutput2[1]
				else:
					result = evaluateArithmeticExpressionOutput4[1]
			else:
				PRINT ("Unknown expression of length",len(inputList)," = ",inputList )
				errorMessage = "Cannot evaluate: Unknown expression of length"+STR(len(inputList))," = " + STR(inputList)
				errorRoutine(errorMessage)
				return [False, None]
				
		elif inputList[0] == "function()":
			errorMessage = "Sorry, function call (including sizeof) not supported yet (coming soon)"
			errorRoutine(errorMessage)
			return [False, None]
		
		else:
			errorMessage = "Cannot evaluate: Unknown expression of length"+STR(len(inputList))," = " + STR(inputList)
			errorRoutine(errorMessage)
			return [False, None]
			
		return [True, result]
		
	else:
		PRINT ("inputList = ", inputList )
		PRINT ("ERROR - inputList not list or numeric string - exiting" )
		errorMessage = "ERROR Cannot evaluate: Unknown expression "+STR(inputList)
		errorRoutine(errorMessage)
		return [False, None]

#inputList = ['7']
#res = evaluateArithmeticExpression(inputList)
#print res
#PRINT (evaluateArithmeticExpression(["1","+",[[['-','3'],'^','2'],'*','5']]) )

	
#######################################################################################################################################################
#This function takes in two lists. It returns a third list, which is essentially setC = setA - setB
#######################################################################################################################################################
def removeItemsIn2ndListFrom1st (a,b):
	c = a.copy()
	for item in b:
		if item in c:
			c.remove(item)
	return c

#######################################################################################################################################################
#This function takes in two lists. It returns a third list, which is essentially setC = setA intersection setB
#######################################################################################################################################################
def commonItems (list1,list2):
	if not (list1 and list2 and isinstance(list1,list) and isinstance(list2,list) ):
		return []
	common = []
	for item in list1:
		if item in list2:
			common.append(item)
	return common


#######################################################################################################################################################
#This function takes in two lists. It returns a third list, which is essentially setC = setA Union setB
#######################################################################################################################################################
def setUnion (list1,list2):
	list1 = [list1] if checkIfString(list1) else list1
	list2 = [list2] if checkIfString(list2) else list2
	
	if not (isinstance(list1,list) and isinstance(list2,list) ):
		warningMessage ="WARNING: Cannot perform set-like union for list1="+STR(list1)+" and list2="+STR(list2)
		warningRoutine(warningMessage)
		return False
	else:
		unionItemList = []
		unionItemList.extend(list1)
		for item in list2:
			if item not in list1:
				unionItemList.append(item)
		return unionItemList



#######################################################################################################################################################
#This function takes in a list of tokens. It finds the ## operators inside them, and then concatenates the tokens accordingly
#######################################################################################################################################################
def applyDoubleHashOperator(inputList):
	PRINT("inputList =",inputList)
	if inputList == [] or checkIfString(inputList):
		return inputList
	elif isinstance(inputList,list):
		# If it is a list of lists, but contains only a single member, remove one level of listification
		if len(inputList) == 1:
			PRINT ("Returning",inputList[0] )
			return applyDoubleHashOperator (inputList[0])
		else:	
			if isinstance(inputList,list) and len(inputList)==3 and inputList[1]=='##':
				concatenatedToken = applyDoubleHashOperator(inputList[0])+applyDoubleHashOperator(inputList[2])
				PRINT("Returning concatenatedToken = <",concatenatedToken,">")
				return concatenatedToken
			else:
				outputList = []
				i = 0
				while i < len(inputList):
					outputList.append(applyDoubleHashOperator(inputList[i]))
					i = i+1
				PRINT("outputList =",outputList)
				return outputList

#lst1 = ['a','##',['b','##','c']]
#lst2 = applyDoubleHashOperator(lst1)
#MUST_PRINT (lst2 )
#sys.exit()



######################################################################################################################################################################
# This function checks if a given list has starts with a brace, whether the matching brace is also there or not (also checks for the legality of interleaving braces).
# After the matched brace is found, it does not care if there are more items in the list, or the legality of its structure thereafter.
######################################################################################################################################################################
def matchingBraceDistance(inputList):
	global bracesDict, bracesDictReverse
	if inputList[0] not in bracesDict:
		PRINT ("Error: inputList[0] begins with a ",inputList[0],", not a proper brace like (,{,[,<, or ?" )
		return -1000000	# An arbitrary large negative number
		sys.exit()

	# Check if the incoming token stream has the different kind of braces legally interleaved or not
	# For example, ((a+b[c])) is fine. ((a+b[c)]) is NOT fine, even though they have the matching count of parenthesis. 
	onlyBraces = []
	i=0
	# There is a problem with the < > braces, since "<" and ">" are also valid operators, which means there might be an mismatching number of them
	# So, we count them only when the inputList[0] is a "<". Same with : and ?
	while i < len(inputList):
		if inputList[i] in bracesDict:
			if (inputList[i]!="<" and inputList[i]!="?") or (inputList[i]=="<" and inputList[0]=="<") or (inputList[i]=="?" and inputList[0]=="?"):
				onlyBraces.append(inputList[i])
		elif inputList[i] in bracesDictReverse:
			if (inputList[i]!=">" and inputList[i]!=":") or (inputList[i]==">" and inputList[0]=="<") or (inputList[i]==":" and inputList[0]=="?"):
				if onlyBraces[-1] == bracesDictReverse[inputList[i]]:
					del onlyBraces[-1]
				else:
					errorMessage = "ERROR in matchingBraceDistance(): Illegal brace \"" + STR(inputList[i]) + "\" found in inputList["+ STR(i) + "], expected a \"" + STR(bracesDict[onlyBraces[-1]]) +"\"" 
					errorRoutine(errorMessage)
					return -1000000	# An arbitrary large negative number
					sys.exit()
		# This assumes that onlyBraces gets populated with the i=0, and the moment it is getting emptied, that means we have found a matching end-parenthesis
		if not onlyBraces:
			return i
		i=i+1
		
	if onlyBraces:
		PRINT ("onlyBraces = ",onlyBraces, "len(onlyBraces) = ",len(onlyBraces) )
		PRINT ("Incomplete input - still expecting a ", bracesDict[onlyBraces[-1]] )
		return -1000000		# An arbitrary large negative number



######################################################################################################################################################################
# This function checks if a given list has ends with a brace, whether the matching brace is also there or not (also checks for the legality of interleaving braces).
# After the matched brace is found, it does not care if there are more items in the list, or the legality of its structure therebefore.
######################################################################################################################################################################
def matchingBraceDistanceReverse(inputList):
	global bracesDict, bracesDictReverse
	if inputList[-1] not in bracesDictReverse:
		PRINT ("Error: inputList[-1] ends with a ",inputList[-1],", not a proper brace like ),},],>, or :" )
		return -100000 	# An arbitrary large negative number
		sys.exit()

	# Check if the incoming token stream has the different kind of braces legally interleaved or not
	# For example, ((a+b[c])) is fine. ((a+b[c)]) is NOT fine, even though they have the matching count of parenthesis. 
	onlyBraces = []
	i=len(inputList)-1
	# There is a problem with the < > braces, since "<" and ">" are also valid operators, which means there might be an mismatching number of them
	# So, we count them only when the inputList[0] is a "<"
	while i >= 0:
		if inputList[i] in bracesDictReverse:
			if inputList[i]!=">" or (inputList[i]==">" and inputList[-1]==">"):
				onlyBraces.append(inputList[i])
		elif inputList[i] in bracesDict:
			if inputList[i]!="<" or (inputList[i]=="<" and inputList[-1]==">"):
				if onlyBraces[-1] == bracesDict[inputList[i]]:
					del onlyBraces[-1]
				else:
					errorMessage = "ERROR in matchingBraceDistanceReverse(): Illegal brace \"" + STR(inputList[i]) + "\" found in inputList["+ STR(i) + "], expected a \"" + STR(bracesDictReverse[onlyBraces[-1]]) +"\"" 
					errorRoutine(errorMessage)
					PRINT ("Error: Illegal brace ",inputList[i], " found in inputList[",i,"], expected a ",bracesDictReverse[onlyBraces[-1]] )
					return -100000 	# An arbitrary large negative number
					sys.exit()
		# This assumes that onlyBraces gets populated with the i=len(inputList)-1, and the moment it is getting emptied, that means we have found a matching end-parenthesis
		if not onlyBraces:
			return len(inputList)-i-1
		i = i - 1
		
	if onlyBraces:
		PRINT ("onlyBraces = ",onlyBraces, "len(onlyBraces) = ",len(onlyBraces) )
		PRINT ("Incomplete input - still expecting a ", bracesDictReverse[onlyBraces[-1]] )
		return -1000000		# An arbitrary large negative number

#list1 = ['a','(','a','+','b','[','c',']',')','b','{','}']
#list2 = ["(","a","(","b","[","+",'(',')',"c","]","-","[","]","e",")",")"]
#list3 = ['(','a','+','b','[','c',')',']']
#list1 = ['(','a',')','b']
#PRINT (matchingBraceDistanceReverse(list2[:10]) )
#sys.exit()


####################################################################################################################################################
# This function takes in a list of tokens (not necessarily an AST) that contains some braces, and it checks the legality of the brace interleaving.
# For example, ((a+b[c])) is fine. ((a+b[c)]) is NOT fine, even though they have the matching count of parenthesis. 
# We are deliberately not including the third braces here, as that might be used as part of Logical operation.
#####################################################################################################################################################
def braceInterleavingLegal(inputList,omitColons = True):
#	PRINT ("Checking <",inputList,"> for brace interleaving legality" )
	global bracesDict, bracesDictReverse
	onlyBraces = []
	i=0
	while i < len(inputList):
		# Since 
		if inputList[i] == "<" or inputList[i] == ">":
			pass
		# Unless there exists the '?', we don't check for the ':'. This is because colons will always be unmatched in a bitfield declaration.
		# The only case where this will create problem is where we have multi-variable declarations like int a:4, b[2+3>3?
		elif (omitColons == True) and (inputList[i] == "?" or inputList[i] == ":"):	
			pass
		elif inputList[i] in bracesDict:
			onlyBraces.append(inputList[i])
		elif inputList[i] in bracesDictReverse:
			if onlyBraces and (onlyBraces[-1] == bracesDictReverse[inputList[i]]):
				del onlyBraces[-1]
			else:
				PRINT ("i =",i,", onlyBraces =",onlyBraces )
				if onlyBraces:
					errorMessage = "ERROR in braceInterleavingLegal(): Illegal brace " + STR(inputList[i]) + " found in inputList[" + STR(i) + "], expected a " + STR(bracesDict[onlyBraces[-1]] )
				else:
					errorMessage = "ERROR in braceInterleavingLegal(): Illegal brace " + STR(inputList[i]) + " found in inputList[" + STR(i) + "], no previous occurence of " + STR(bracesDictReverse[inputList[i]] )
				errorRoutine(errorMessage)
				return False
		i = i + 1
	if onlyBraces:
		return False
	else:
		return True
		
#list1 = ['a','(','a','+','b','[','c',']',')','b','{','}']
#list2 = ['(','a','+','b','[','c',')',']']
#PRINT (braceInterleavingLegal(list1) )
#PRINT (braceInterleavingLegal(list2) )
#sys.exit()
#####################################################################################################################################
# findSubsequenceInList(subsequence, tokenList)
# This routine finds if the first list exists as a subsequence of the second list. If it does, it sends the first occurrence of that.
# And the result is a list of the indices (not necessarily contiguous) of the tokenList that correspond to the subsequence.
# For example, the [c,f,g] subsequence exists in a list [a,b,c,d,e,f,g,h,i]. This routine will return [2,5,6].
######################################################################################################################################

def findSubsequenceInList(subsequence, tokenList):
	PRINT("Looking for susquence =",subsequence,"in tokenList =",tokenList)
	if not isinstance(subsequence,list):
		errorMessage = "input subsequence "+STR(subsequence)+" is not a list"
		errorRoutine(errorMessage)
		return False
	if not isinstance(tokenList,list):
		errorMessage = "input tokenList "+STR(tokenList)+" is not a list"
		errorRoutine(errorMessage)
		return False
	
	if len(subsequence) == 0:
		return []
	elif len(subsequence) > len(tokenList):
		return []
	elif len(subsequence) == len(tokenList) and subsequence != tokenList:
		return []
	elif subsequence[0] not in tokenList:
		return []
	elif len(subsequence)==1:
		return [tokenList.index(subsequence[0])]
	else:
		foundAtIndex = -1
		while subsequence[0] in tokenList[foundAtIndex+1:]:
			foundAtIndex = foundAtIndex+1 + tokenList[foundAtIndex+1:].index(subsequence[0])
			PRINT("Found occurrence of ",subsequence[0],"at position",foundAtIndex,"of ",tokenList)
			tempList = []
			result = findSubsequenceInList(subsequence[1:], tokenList[foundAtIndex+1:])
			PRINT("findSubsequenceInList(",STR(subsequence[1:]),",", STR(tokenList[foundAtIndex+1:]),") =",STR(result))
			if result!=False and result != []:
				if len(result) != len(subsequence)-1:
					OUTPUT("Coding error in findSubsequenceInList(), result is ",result,"while subsequence =",subsequence)
					sys.exit()
				tempList = [foundAtIndex]
				for item in result:
					tempList.append(item+foundAtIndex+1)
				break
		# Verify that the result is correct
		if tempList != []:
			if len(tempList) != len(subsequence):
				OUTPUT("Coding error in findSubsequenceInList(), result is ",tempList,"while subsequence =",subsequence,"and they are of different length")
				sys.exit()
			else:
				for i in range(len(tempList)):
					if subsequence[i] != tokenList[tempList[i]]:
						OUTPUT("Coding error in findSubsequenceInList(), result[",i,"] = ",tempList[i],"but tokenList[",tempList[i],"] =",tokenList[tempList[i]],"doesn't match with subsequence[",i,"] =",subsequence[i])
						sys.exit()
		return tempList
	
###########################################################################################################################################
# Checks if the tokenlist contains a function definition (NOT declaration) of the form:    funcname([arguments]){[statements]}
###########################################################################################################################################
def checkIfFunctionDefinition(tokenList):
	PRINT("Checking for function signature in tokenList =",STR(tokenList))
	if not isinstance(tokenList,list):
		return [False, None]
	
	# Kludge - I have implemented the '()' operator also, so 
	functionDefinitionSignature1 = ['(',')','{','}']
	functionDefinitionSignature2 = ['()','{','}']
	functionDefinitionSignature = [functionDefinitionSignature1, functionDefinitionSignature2]
	functionCheckResult = False
	functionDefinitionEndIndex = LARGE_NEGATIVE_NUMBER

	result = findSubsequenceInList(functionDefinitionSignature1, tokenList)
	if result != False and result != []:
		if result[1] != result[2]-1:	# The { must come right after the closing )
			PRINT("The } did not come right before the { - hence no function")
		else:
			# check if the () braces match
			d1 = matchingBraceDistance(tokenList[result[0]:])
			d2 = matchingBraceDistance(tokenList[result[2]:])
			if d1 < 0:
				PRINT("No matching ) for ( - hence no function")
			elif result[0] + d1 != result[1]:
				PRINT("There exists a } but that doesn't match with the ( - hence no function")
			
			# check if the {} braces match
			elif d2 < 0:
				PRINT("No matching } for { - hence no function")
			elif result[2] + d2 != result[3]:
				PRINT("There exists a } but that doesn't match with the { - hence no function")
				
			# Check if the token right before the ( is not a keyword
			elif result[0] == 0 or tokenList[result[0]-1] in illegalVariableNames:
				PRINT("The token before the ( } is not a proper variable name - hence no function")
			
			else:
				functionCheckResult = True
				functionDefinitionEndIndex = result[3]

	if functionCheckResult == False:
		result = findSubsequenceInList(functionDefinitionSignature2, tokenList)
		if result != False and result != []:
			# check if the () braces match
			d2 = matchingBraceDistance(tokenList[result[1]:])
			
			# check if the {} braces match
			if d2 < 0:
				PRINT("No matching } for { - hence no function")
			elif result[1] + d2 != result[2]:
				PRINT("There exists a } but that doesn't match with the { - hence no function")
				
			# Check if the token right before the ( is not a keyword
			elif result[0] == 0 or tokenList[result[0]-1] in illegalVariableNames:
				PRINT("The token before the ( } is not a proper variable name - hence no function")
			else:
				functionCheckResult = True
				functionDefinitionEndIndex = result[2]

	PRINT("functionCheckResult =",functionCheckResult,"for tokenList =",STR(tokenList))

	#Sanity check
	if functionCheckResult == True: 
		if tokenList[functionDefinitionEndIndex] != '}':
			OUTPUT("Coding error in checkIfFunctionDefinition() - exiting")
			sys.exit()
		else:
			return [True, functionDefinitionEndIndex]
	else:
		return [False, None]

####################################################################################################################################################
# This function takes in a list of tokens which represent the parenthesized comma-separated list of arguments, and returns a list of the arguments
# In the returned list of list, each list is an argument, which itself is a list of tokens
# Thus, parseArgumentList(["(","a",",","(","b",",","c",")",")"]) will yield [['a'], ['(', 'b', ',', 'c', ')']]
#####################################################################################################################################################
def parseArgumentList(inputList, omitColons=False):
	global bracesDict, bracesDictReverse
	if not (len(inputList)>=2 and ((inputList[0] =='(' and inputList[-1]==')') or (inputList[0] =='{' and inputList[-1]=='}'))):
		PRINT ("Invalid argument list - must be properly parenthesized",inputList )
		return False
		sys.exit()
	# Check if the incoming token stream has the different kind of braces legally interleaved or not
	# For example, ((a+b[c])) is fine. ((a+b[c)]) is NOT fine, even though they have the matching count of parenthesis. 
	argumentList = []
	onlyBraces = []
	if len(inputList)==2:
		return argumentList
	
	# Here we assume that we have at least one argument
	# To-DO : Strip away the spaces, unless it is all spaces
	argStartIndex = 1
	i=0
	while i < len(inputList):
		if omitColons and inputList[i] in ('?',':'):
			pass
		elif inputList[i] in bracesDict:
			onlyBraces.append(inputList[i])
		elif inputList[i] in bracesDictReverse:
			#Special case for ending parenthesis
			if i==len(inputList)-1 and inputList[i] in (')','}'):
				if argStartIndex==i-1: # If it is a single member, no point making it a list
					argumentList.append(inputList[argStartIndex])
				else:
					argumentList.append(inputList[argStartIndex:i])
			elif onlyBraces[-1] == bracesDictReverse[inputList[i]]:
				del onlyBraces[-1]
			else:
				errorMessage = "ERROR in parseArgumentList("+STR(inputList)+"): Illegal brace \"" + STR(inputList[i]) + "\" found in inputList[" +STR(i) + "], expected a \"" + STR(bracesDict[onlyBraces[-1]])+ "\""
				errorRoutine(errorMessage)
				return False
				sys.exit()
		elif len(onlyBraces)==1 and onlyBraces[-1] in ('(','{') and (inputList[i] == ',' or i==len(inputList)-1):
			if argStartIndex==i-1: # If it is a single member, no point making it a list
				argumentList.append(inputList[argStartIndex])
			else:
				argumentList.append(inputList[argStartIndex:i])
			argStartIndex = i+1
		i=i+1
	return argumentList

#PRINT (parseArgumentList(["(","a",",","(","b",",","c",")",")"]) )
	
#PRINT (parseArgumentList(["(","a","(","b","[","+","c","]","-","[","]","e",")"]) )
#sys.exit()	


#######################################################################################################################################################################
# This recursive function takes three arguments.: 1) One input list, 2) list item to be replaced (which is A) 3) the new list item that it will replace it (which is B)
########################################################################################################################################################################
def replaceToken (inputList, A, B):
	if isinstance(inputList, list):
		inputListCopy = []
		for item in inputList:
#			PRINT ("Before traversal, item = <",item,">" )
			inputListCopy.append(replaceToken (item, A, B))
#			PRINT ("After traversal, item = <",item,">" )
		return inputListCopy
	else:
		if inputList == A:
#			PRINT ("Before replacement, inputList = <",inputList,">" )
			inputList = B
#			PRINT ("After replacement, inputList = <",inputList,">" )
		return inputList

##########################################################################################################################################################
# This function takes three arguments.: 1) One input list, 2) A dictionary <key,value> pairs so that 
# all the <key_i> values should be replaced with the corresponding <value_i> values. We implement the dictionary using list since dictionary is un
# We cannot do this just by replacing the tokens. Because then suppose the dictionary contains two key-value pairs: <a,b> and <b,c>
# which means replace all a's with b's, and replace all b's with c's. So, we would expect an expression of a+b to be transformed to b+c.
# Unfortunately, if we do this by first doing a-->b replacement, we will get (a+b)-->(b+b). Now if we do the b-->c replacement, we will get (c+c).
# To avoid this problem, we must design the problem the following way: Make sure that the key set and value set never intersect.
# To achieve this without having to look at all possible invocations of a macro, we should first change the macro arguments to somethings
# that the macro invocations would never use. This is the first step. Once this first step is complete, we can do the second step of replacing the
# never-used-in-invocations-variables to actual-invocation-variable-argument-variables.
##########################################################################################################################################################
# The output is a 2-member tuple. The first member tells if this the return value is True or False. If True, only then one should pay attention to the 2nd member, the result.
# The reason we do this convoluted way is beacuse we are worried that a simple return value of False might be construed as a valid return result.
##########################################################################################################################################################

def replaceArguments (inputList, dictionary):
	if isinstance(dictionary,dict):
		newDict = OrderedDict()
		newDict1stHalf = OrderedDict()
		newDict2ndHalf = OrderedDict()
		
		# Choose a very arbitrary prefix that will NEVER be an actual variable name. If it still appears in one of <value>s, keep changing it until it doesn't
		prefix = "______Z___Ta_9UYTadfg_____"
		while (True):
			prefixAppearsInValues = False
			for key,value in dictionary.items():
				outputTextArithmeticExpressionFromASTOutput = outputTextArithmeticExpressionFromAST(value)
				if outputTextArithmeticExpressionFromASTOutput == False:
					PRINT ("ERROR in replaceArguments after calling outputTextArithmeticExpressionFromAST(value) for value =", value )
					return [False,None]
				if outputTextArithmeticExpressionFromASTOutput.find(prefix) >= 0:
					PRINT ("prefix", prefix, "found in value <",value,">" )
					prefixAppearsInValues = True
					break
			if prefixAppearsInValues == True:
				prefix = "_" + prefix  + "_"
			else:
				break
		PRINT ("prefix = <",prefix,">" )
		
		for key,value in dictionary.items():
			# Check that the key values are never a list. Otherwise we cannot really assign the prefix to a list
			if not checkIfString(key):
				PRINT ("Error: Inside Macro arguments definitions, arguments must be a single string variable, where it is now <",key,">" )
				return [False, None]
				sys.exit()
			else:
				newDict1stHalf[key] = prefix+key
				newDict2ndHalf[prefix+key] = value

		# It's important that we do it this way. Otherwise, we will still have the intended problem we are doing to solve
		for key, value in newDict1stHalf.items():
			newDict[key]=value
		for key, value in newDict2ndHalf.items():
			newDict[key]=value
		PRINT (newDict )
		
		for key,value in newDict.items():
			inputList = replaceToken (inputList, key, value)
	return [True, inputList]

###################################################################################
# Convert Multi-Line Strings into Single-Line Strings	
###################################################################################
def convertMultiLineStringsIntoSingleLineStrings(inputLines):
	if not inputLines:
		return []
	
	# Check that inputLines is a list of lines (strings ending with a newline). If it is a single string, make it a list
	if  isinstance(inputLines,list):
#		PRINT ("inputLines is indeed a list" )
		itemCount = 0
		while itemCount < len(inputLines):
			if not checkIfString(inputLines[itemCount]):
				PRINT ("Exiting - inputLines is not a list of proper strings - ", inputLines )
				return False
				sys.exit()
			elif not inputLines[itemCount] or inputLines[itemCount][-1] != '\n':
#				PRINT ("Appending newline to the end of inputLines[",itemCount,"]" )
				inputLines[itemCount] = inputLines[itemCount] + '\n'
			itemCount = itemCount + 1
		PRINT ("inputLines is indeed a list of proper strings - ", inputLines )
	else:
#		PRINT ("inputLines is NOT a list" )
		if checkIfString(inputLines):
#			PRINT (("Checking if inputLines=<%s> has a newline at the end"%(inputLines)) )
			if inputLines[-1] != '\n':
#				PRINT ("Appending newline to the end of inputLines" )
				inputLines = inputLines + '\n'
#			PRINT ("Converting the inputLines <",inputLines,">, which is a basic string but not a list, into a list" )
			inputLines = [inputLines]
#			PRINT ("Now the listified inputLines = ",inputLines )
		else:
			PRINT ("Exiting - Unknown object type - inputLines = <",inputLines,">" )
			return False
			sys.exit()
	
	outputLines = inputLines
	
	continuingString = False
	stringStartLineNum = LARGE_NEGATIVE_NUMBER
	stringStartCharNum = LARGE_NEGATIVE_NUMBER
	stringEndLineNum   = LARGE_NEGATIVE_NUMBER
	stringEndCharNumInclusive   = LARGE_NEGATIVE_NUMBER
	
	lineNum = 0
	while True:
		if lineNum>=len(inputLines):
			break
		else: 
			PRINT("Processing line #",lineNum," = ",inputLines[lineNum])
			pass
		line = inputLines[lineNum]
		for i in range(len(line)):
			if line[i] == '"':
				if continuingString:
					if i>0 and line[i-1]=="\\":
						pass
					else: #End of string
						stringEndLineNum   = lineNum
						stringEndCharNumInclusive   = i
						
						if stringEndLineNum == stringStartLineNum:	# String starts and ends on the same line; do nothing
							pass
						elif stringEndLineNum < stringStartLineNum: # Error
							errorMessage = "ERROR in convertMultiLineStringsIntoSingleLineStrings: stringEndLineNum (%d) < stringStartLineNum (%d)"%(stringEndLineNum, stringStartLineNum)
							errorRoutine(errorMessage)
							return False
						elif stringEndLineNum > stringStartLineNum: # 
							#Convert the outputlines
							for j in range(len(outputLines)):
								if outputLines[j][-1] != "\n":
									OUTPUT("Line",j, "does not end with newline - exiting")
									sys.exit()
								if j < stringStartLineNum or j > stringEndLineNum:
									pass
								elif j == stringStartLineNum:
									outputLines[stringStartLineNum] = outputLines[stringStartLineNum][:-1] + "\\n"
								elif stringStartLineNum < j < stringEndLineNum:
									outputLines[stringStartLineNum] += outputLines[j]
									outputLines[stringStartLineNum]= outputLines[stringStartLineNum][:-1]+"\\n"
									outputLines[j] = "\n"
								elif j == stringEndLineNum:
									outputLines[stringStartLineNum] += outputLines[j][:stringEndCharNumInclusive+1]
									outputLines[stringStartLineNum] += "\\n"
									outputLines[stringEndLineNum] = " "*(stringEndCharNumInclusive+1) + inputLines[stringEndLineNum][stringEndCharNumInclusive+1:]
								else:
									OUTPUT("Coding bug")
									sys.exit()
									
						else:
							OUTPUT("Coding bug")
							sys.exit()
						
						# Reset these values						
						stringStartLineNum = LARGE_NEGATIVE_NUMBER
						stringStartCharNum = LARGE_NEGATIVE_NUMBER
						stringEndLineNum   = LARGE_NEGATIVE_NUMBER
						stringEndCharNumInclusive   = LARGE_NEGATIVE_NUMBER
						
				else:	# Start of string
						stringStartLineNum   = lineNum
						stringStartCharNum   = i
						continuingString = True
	
		lineNum += 1
		
	return 	outputLines

#inputLines = ['x = "Hi \n', ' there, \n', 'my friend!"; int y;\n']
#outputLines = convertMultiLineStringsIntoSingleLineStrings(inputLines)
#PRINT("inputLines =",inputLines)
#MUST_PRINT("outputLines =",outputLines)
#sys.exit()

###################################################################################
# Convert Single-Line Strings into Multi-Line Strings	
###################################################################################
def convertSingleLineStringsIntoMultiLineStrings(inputLines):
	if not inputLines:
		return []
	
	# Check that inputLines is a list of lines (strings ending with a newline). If it is a single string, make it a list
	if  isinstance(inputLines,list):
#		PRINT ("inputLines is indeed a list" )
		itemCount = 0
		while itemCount < len(inputLines):
			if not checkIfString(inputLines[itemCount]):
				PRINT ("Exiting - inputLines is not a list of proper strings - ", inputLines )
				return False
				sys.exit()
			elif not inputLines[itemCount] or inputLines[itemCount][-1] != '\n':
#				PRINT ("Appending newline to the end of inputLines[",itemCount,"]" )
				inputLines[itemCount] = inputLines[itemCount] + '\n'
			itemCount = itemCount + 1
		PRINT ("inputLines is indeed a list of proper strings - ", inputLines )
	else:
#		PRINT ("inputLines is NOT a list" )
		if checkIfString(inputLines):
#			PRINT (("Checking if inputLines=<%s> has a newline at the end"%(inputLines)) )
			if inputLines[-1] != '\n':
#				PRINT ("Appending newline to the end of inputLines" )
				inputLines = inputLines + '\n'
#			PRINT ("Converting the inputLines <",inputLines,">, which is a basic string but not a list, into a list" )
			inputLines = [inputLines]
#			PRINT ("Now the listified inputLines = ",inputLines )
		else:
			OUTPUT ("Exiting - Unknown object type - inputLines = <",inputLines,">" )
			return False
			sys.exit()

	outputLines = inputLines
	
	continuingString = False
	stringStartLineNum = LARGE_NEGATIVE_NUMBER
	stringStartCharNum = LARGE_NEGATIVE_NUMBER
	stringEndLineNum   = LARGE_NEGATIVE_NUMBER
	stringEndCharNumInclusive   = LARGE_NEGATIVE_NUMBER
	
	lineNum = 0
	while True:
		if lineNum>=len(inputLines):
			break
		else: 
			PRINT("Processing line #",lineNum," = ",inputLines[lineNum])
			pass
		line = inputLines[lineNum]
		for i in range(len(line)):
			if line[i] == '"':
				if continuingString:
					if i>0 and line[i-1]=="\\":
						pass
					else: #End of string
						stringEndLineNum   = lineNum
						stringEndCharNumInclusive   = i
						
						if stringEndLineNum != stringStartLineNum:	# String does not start and end on the same line; error
							errorMessage = "ERROR in convertSingleLineStringsIntoMultiLineStrings: stringEndLineNum (%d) != stringStartLineNum (%d)"%(stringEndLineNum, stringStartLineNum)
							errorRoutine(errorMessage)
							return False
						elif "\\n" not in line[stringStartCharNumInclusive:stringEndCharNumInclusive+1]: # simple string, do nothing
							pass
						else:
							stringToSplit = line[stringStartCharNumInclusive:stringEndCharNumInclusive+1]
							splitString = stringToSplit.split("\\n")
							if len(splitString) <= 1:
								errorMessage = "ERROR in convertSingleLineStringsIntoMultiLineStrings: expecting at least one newline in string <%s>"%stringToSplit
								errorRoutine(errorMessage)
								return False
								
							#Convert the outputlines (TBD - not done)
							for j in range(len(outputLines)):
								if outputLines[j][-1] != "\n":
									OUTPUT("Line",j, "does not end with newline - exiting")
									sys.exit()
								if j < stringStartLineNum or j > stringEndLineNum:
									pass
								elif j == stringStartLineNum:
									outputLines[stringStartLineNum] = outputLines[stringStartLineNum][:-1] + "\\n"
								elif stringStartLineNum < j < stringEndLineNum:
									outputLines[stringStartLineNum] += outputLines[j]
									outputLines[stringStartLineNum]= outputLines[stringStartLineNum][:-1]+"\\n"
									outputLines[j] = "\n"
								elif j == stringEndLineNum:
									outputLines[stringStartLineNum] += outputLines[j][:stringEndCharNumInclusive+1]
									outputLines[stringStartLineNum] += "\\n"
									outputLines[stringEndLineNum] = " "*(stringEndCharNumInclusive+1) + inputLines[stringEndLineNum][stringEndCharNumInclusive+1:]
								else:
									OUTPUT("Coding bug")
									sys.exit()
									
					
						# Reset these values						
						stringStartLineNum = LARGE_NEGATIVE_NUMBER
						stringStartCharNum = LARGE_NEGATIVE_NUMBER
						stringEndLineNum   = LARGE_NEGATIVE_NUMBER
						stringEndCharNumInclusive   = LARGE_NEGATIVE_NUMBER
						
				else:	# Start of string
						stringStartLineNum   = lineNum
						stringStartCharNum   = i
						continuingString = True
	
		lineNum += 1
		
	return 	outputLines


######################################################################################	
# TO-DO: How to handle newlines (our program is not consistent on this)
#
# When this is called, we have already called preProcess(), which has removed comments and converted multiline macros into single line.
#
# It outputs a list of the following things: 

# 1) A simple list of string tokens (only this thing is being used now)
# 2) List of tokens, but for each token, we include yet another list of all the occurrences. Mostly used for multi-line tokens.
# 3) A linewise list of tokens with lots of informations (like from which line and char they start and end, whether the tokens are starting/ending
######################################################################################	

def tokenizeLines(lines):
#	global preprocessingDirectives, twoCharOperatorList, threeCharOperatorList
	tokenList = []	# A simple list of string tokens (only this thing is being used now)
	tokenListInfo = []	# List of tokens, but for each token, we include yet another list of all the occurrences. Mostly used for multi-line tokens.
	linewiseTokenInfo = []	# tells for every line, [token, overall token#, starting line#, starting char#, ending line#, ending char# (inclusive), whethere the token starts/ends on this line]
	currentToken = ""
	lineNumber = -1
	continuingMacro = False

	if not lines:
		return [[],[],[]]
	
	# Check that lines is a list of Lines (strings ending with a newline). If it is a single string, make it a list
	if  isinstance(lines,list):
#		PRINT ("lines is indeed a list" )
		itemCount = 0
		while itemCount < len(lines):
			if not checkIfString(lines[itemCount]):
				PRINT ("Exiting - lines is not a list of proper strings - ", lines )
				return False
				sys.exit()
			elif not lines[itemCount] or lines[itemCount][-1] != '\n':
#				PRINT ("Appending newline to the end of lines[",itemCount,"]" )
				lines[itemCount] = lines[itemCount] + '\n'
			itemCount = itemCount + 1
#		PRINT ("lines is indeed a list of proper strings - ", lines )
	else:
#		PRINT ("lines is NOT a list" )
		if checkIfString(lines):
#			PRINT (("Checking if lines=<%s> has a newline at the end"%(lines)) )
			if lines[-1] != '\n':
#				PRINT ("Appending newline to the end of lines" )
				lines = lines + '\n'
#			PRINT ("Converting the lines <",lines,">, which is a basic string but not a list, into a list" )
			lines = [lines]
#			PRINT ("Now the listified lines = ",lines )
		else:
			PRINT ("Exiting - Unknown object type - lines = <",lines,">" )
			return False
			sys.exit()
	
	tokenIndex = 0		# Total token count = 1 + max(tokenIndex). This is NOT just within a single line, it is for ALL the lines overall
	
	currentTokenStartLineNum = LARGE_NEGATIVE_NUMBER
	currentTokenStartCharNum = LARGE_NEGATIVE_NUMBER
	currentTokenEndLineNum = LARGE_NEGATIVE_NUMBER
	currentTokenEndCharNumInclusive = LARGE_NEGATIVE_NUMBER
		
	
	for line in lines:
	
		lineNumber += 1
		currentLinetokenList = []
		currentLineTokenListInfo = []		# each item is a list of <currentToken, currentTokenStartCharNum, currentTokenEndCharNumInclusive>
		i = 0
		continuingString = False	# In Standard C, a string is demarcated by a double-quote
		continuingChar = False	# In Standard C, a char is demarcated by a single-quote
		currentLineIsHashDefine = False
		
		while i < len(line):	# Process all the chars within this current line
			c = line[i]
			if c:
				if continuingString == True and continuingChar == True:
					errorMessage = "We cannot have conntinuation of both single-quoted and double-quoted string"
					errorRoutine(errorMessage)
					return False
				elif continuingString == True or continuingChar == True:
					currentToken += c
					# Ending a string liternal token
					if c in ('"','\'') and currentToken[-2]!="\\":	# TO-DO should not it be -2 instead of -1, since we already added the double-quote char?
						if c == '"':
							continuingString = False
						if c == '\'':
							continuingChar = False
							
						currentLinetokenList.append(currentToken)
						currentTokenEndLineNum = lineNumber
						currentTokenEndCharNumInclusive = i
						currentLineTokenListInfo.append([currentToken, tokenIndex, currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive])
						currentTokenStartLineNum = LARGE_NEGATIVE_NUMBER
						currentTokenStartCharNum = LARGE_NEGATIVE_NUMBER
						currentTokenEndLineNum = LARGE_NEGATIVE_NUMBER
						currentTokenEndCharNumInclusive = LARGE_NEGATIVE_NUMBER
						currentToken = ""
						tokenIndex += 1
				elif c in ('"','\''):		# The assumption is that the string liternal starts here
						currentToken += c
						if c == '"':
							continuingString = True
						elif c == '\'':
							continuingChar = True
						else:
							sys.exit()
						currentTokenStartLineNum = lineNumber
						currentTokenStartCharNum = i
						currentTokenEndCharNumInclusive = i
#				elif (currentToken == "" and re.search('[#A-Za-z0-9_]',c)) or (currentToken != "" and re.search('[A-Za-z0-9_]',c)):		# Alphanumeric (and preprocessor directives)
				elif re.search('[A-Za-z0-9_]',c):		# Alphanumeric (and preprocessor directives)
					if currentToken == "":	# The token starts here
						currentTokenStartLineNum = lineNumber
						currentTokenStartCharNum = i
					currentToken += c
					currentTokenEndCharNumInclusive = i
				elif c == '.' and currentToken.isdigit() and '.' not in currentToken:
					if currentToken == "":	# The token starts here
						currentTokenStartLineNum = lineNumber
						currentTokenStartCharNum = i
					currentToken += c
					currentTokenEndCharNumInclusive = i
				elif re.search('\s',c):					# Whitespace characters
					if currentToken != "":
						if currentToken == "long" and currentLinetokenList and currentLinetokenList[-1]=="long":
							del currentLinetokenList[-1]
							currentToken = "long long"
							currentTokenStartLineNum = currentLineTokenListInfo[-1][2]	# We need to pick up the starting position from the previous token
							currentTokenStartCharNum = currentLineTokenListInfo[-1][3]	# We need to pick up the starting position from the previous token
						currentLinetokenList.append(currentToken)
						currentTokenEndLineNum = lineNumber
						currentTokenEndCharNumInclusive = i-1		# Do not count the whitespace TO-DO: What about first char in current line is whitespace?
						currentLineTokenListInfo.append([currentToken, tokenIndex, currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive])
						currentTokenStartLineNum = LARGE_NEGATIVE_NUMBER
						currentTokenStartCharNum = LARGE_NEGATIVE_NUMBER
						currentTokenEndLineNum = LARGE_NEGATIVE_NUMBER
						currentTokenEndCharNumInclusive = LARGE_NEGATIVE_NUMBER
						if currentToken in preprocessingDirectives:
							currentLineIsHashDefine = True
						currentToken = ""
						tokenIndex += 1
						
				elif ord(c) >= 32 and ord(c) <= 126:	# Other non-alphanumeric valid characters like the !, #, $, &, ', (, ), {,}, *, +, comma, -, ., /, :, ;, <, =, >, ?, `, ~
				
					if currentToken != "":	# The current char cannot be added to the existing token, so first add the current token
						currentLinetokenList.append(currentToken)
						currentTokenEndLineNum = lineNumber
#						currentTokenEndCharNumInclusive = i
						currentLineTokenListInfo.append([currentToken, tokenIndex, currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive])
						currentTokenStartLineNum = LARGE_NEGATIVE_NUMBER
						currentTokenStartCharNum = LARGE_NEGATIVE_NUMBER
						currentTokenEndLineNum = LARGE_NEGATIVE_NUMBER
						currentTokenEndCharNumInclusive = LARGE_NEGATIVE_NUMBER
						if currentToken in preprocessingDirectives:
							currentLineIsHashDefine = True
							PRINT ("This line is preprocessor stuff" )
						currentToken = ""
						tokenIndex += 1

					# Find out if this is a single-char token, or not
					tokenConsumed = c
					singleCharToken = True
					lastCharIndexToBeConsumedInThisToken = i
					for keyword in keywordsSorted:
						keywordLength = len(keyword)
						if i+keywordLength <= len(line) and line[i:i+keywordLength]==keyword:
							singleCharToken = False
							lastCharIndexToBeConsumedInThisToken = i+keywordLength-1
							tokenConsumed = line[i:lastCharIndexToBeConsumedInThisToken+1]
							break

					# The '#' has a special case. When we have '#define' at the beginning of the line, it is a single token.
					# But, the statement '#define NEWMACRO(define) #define' is valid, and the second '#define' is interpreted as two tokens: '#' followed by 'define'.
					# However, the '##' can be anywhere - leave that alone.
					if c == '#' and singleCharToken == False and tokenConsumed != '##' and line[0:i+1].strip() != '#':
						PRINT("\nVERY, VERY special case found!!")
						lastCharIndexToBeConsumedInThisToken = i
						tokenConsumed = c

					currentLinetokenList.append(tokenConsumed)
					currentTokenStartLineNum = lineNumber
					currentTokenStartCharNum = i
					currentTokenEndLineNum = lineNumber
					currentTokenEndCharNumInclusive = lastCharIndexToBeConsumedInThisToken
					currentLineTokenListInfo.append([tokenConsumed, tokenIndex, currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive])
					tokenIndex += 1
					i = lastCharIndexToBeConsumedInThisToken

					# We do not need to explicitly set the currentToken to "" because if it were not blank, we would deal with it first and make it blank.
					# Observe that we are directly adding the char c (not the currentToken) to the currentLinetokenList and currentLineTokenListInfo
					currentTokenStartLineNum = LARGE_NEGATIVE_NUMBER
					currentTokenStartCharNum = LARGE_NEGATIVE_NUMBER
					currentTokenEndLineNum = LARGE_NEGATIVE_NUMBER
					currentTokenEndCharNumInclusive = LARGE_NEGATIVE_NUMBER
					
				else:
					OUTPUT ("Exiting - unknown character <%s> at char index of (%d) within line=<%s>" %(c,i,line) )
					sys.exit()
					return False
				
				#Takes care of the case where the line ends without a whitespace or newline at the end
				if i == len(line)-1 and currentToken != "":
#					PRINT ("hit i=",i,", the last character <",c,">" )
					currentLinetokenList.append(currentToken)
					currentTokenEndLineNum = lineNumber
					currentTokenEndCharNumInclusive = i
					currentLineTokenListInfo.append([currentToken, tokenIndex, currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive])
					currentTokenStartLineNum = LARGE_NEGATIVE_NUMBER
					currentTokenStartCharNum = LARGE_NEGATIVE_NUMBER
					currentTokenEndLineNum = LARGE_NEGATIVE_NUMBER
					currentTokenEndCharNumInclusive = LARGE_NEGATIVE_NUMBER
					currentToken = ""
					tokenIndex += 1
#					PRINT ("Hit EOL" )
				
				
			else:
				OUTPUT ("HOW DID THE CONTROL COME HERE?" )
				sys.exit()
				if currentToken != "":
					currentLinetokenList.append(currentToken)
					currentTokenEndCharNumInclusive = currentTokenStartCharNum + len(currentToken)
					currentLineTokenListInfo.append([currentToken, tokenIndex, currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive])
					currentTokenStartLineNum = LARGE_NEGATIVE_NUMBER
					currentTokenStartCharNum = LARGE_NEGATIVE_NUMBER
					currentTokenEndLineNum = LARGE_NEGATIVE_NUMBER
					currentTokenEndCharNumInclusive = LARGE_NEGATIVE_NUMBER
					currentToken = ""
					tokenIndex += 1
				PRINT ("Hit EOL" )
				break
				
			i += 1	# Within the current line, increase the char pointer
			
		if (currentLineIsHashDefine or continuingMacro) and currentLinetokenList[-1] =="\\":
			del currentLinetokenList[-1]
			if currentLineTokenListInfo[-1][0] == "\\":
				del currentLineTokenListInfo[-1]
			continuingMacro = True
		elif (currentLineIsHashDefine or continuingMacro) and currentLinetokenList[-1] !="\\":
			continuingMacro = False
			
		PRINT ("For Line # ", lineNumber, ", currentLinetokenList = ", currentLinetokenList )
		tokenList.extend (currentLinetokenList)
		PRINT("\nFor currentLineTokenListInfo below, each member is a tuple <currentToken, tokenIndex, currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive>","\n","="*50)
		PRINT ("For Line # ", lineNumber, ", currentLineTokenListInfo = ", currentLineTokenListInfo )
		linewiseTokenInfo.append (currentLineTokenListInfo)

	# Check that tokenListInfo and linewiseTokenInfo are lists of lists
	


	# Sanity check - verify that tokenList and tokenListInfo are in order

	
	tokenListReconstructed = []
	lastTokenIndex = -1
	tokenIndexListFromLines = []
	for tokenListInfoForOneLine in linewiseTokenInfo:
		PRINT("\nCurrently handling tokenListInfoForOneLine =",tokenListInfoForOneLine)
		i = 0
		while i < len(tokenListInfoForOneLine):
			PRINT("\nCurrently handling tokenListInfoForOneLine[",i,"] =",tokenListInfoForOneLine[i])
			if tokenListInfoForOneLine[i]:	# Not blank
				token = tokenListInfoForOneLine[i][0]
				tokenIndex = tokenListInfoForOneLine[i][1]
				if tokenIndex not in tokenIndexListFromLines:
					tokenIndexListFromLines.append(tokenIndex) 
				currentTokenStartLineNum = tokenListInfoForOneLine[i][2]
				currentTokenStartCharNum = tokenListInfoForOneLine[i][3]
				currentTokenEndLineNum = tokenListInfoForOneLine[i][4]
				currentTokenEndCharNumInclusive = tokenListInfoForOneLine[i][5]
				
				PRINT("For tokenListInfoForOneLine[",i,"], token =", token, "tokenIndex =",tokenIndex)
				if tokenIndex != lastTokenIndex:
					tokenListInfo.append([token, tokenIndex, [[currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive]]])
					tokenListReconstructed.append(token)
					lastTokenIndex = tokenIndex
				else:
					PRINT("WARNING: tokenIndex (", tokenIndex, " == lastTokenIndex (", lastTokenIndex,")!!")
					tokenListInfo[-1][2].append([currentTokenStartLineNum, currentTokenStartCharNum, currentTokenEndLineNum, currentTokenEndCharNumInclusive])
					
			else:
				PRINT("\nWARNING: tokenListInfoForOneLine[",i,"] is blank!!")
			i += 1

	PRINT("\n\n\ntokenList =",tokenList)
	PRINT("\n\n\ntokenListInfo =",tokenListInfo)
	PRINT("\n\nlinewiseTokenInfo =",linewiseTokenInfo)
	
	if tokenList != tokenListReconstructed or len(tokenListInfo) != len(tokenList) or (tokenIndexListFromLines and max(tokenIndexListFromLines)!= len(tokenList)-1):
		OUTPUT("\n\n\nERROR: Mismatching tokenList and tokenListReconstructed!!!")
		OUTPUT("\n\ntokenIndexListFromLines =",tokenIndexListFromLines)
		OUTPUT("\nmax(tokenIndexListFromLines)=",max(tokenIndexListFromLines),"len(tokenList)-1=", len(tokenList)-1)
		OUTPUT("\n\n\nlinewiseTokenInfo =",linewiseTokenInfo)
		OUTPUT("\n\n\ntokenListReconstructed =",tokenListReconstructed)
		OUTPUT("\n\n\ntokenList =",tokenList)
		errorMessage = "The token indices from tokenList, tokenListInfo and linewiseTokenInfo are out of sync!"
		errorRoutine(errorMessage)
		return False
	for i in range(len(tokenList)):
		if tokenList[i] != tokenListInfo[i][0] or i != tokenListInfo[i][1]:
			PRINT("\n\ntokenList =",STR(tokenList))
			PRINT("\n\ntokenListInfo =",STR(tokenListInfo))
			errorMessage = "tokenList and tokenListInfo are out of sync!"
			errorRoutine(errorMessage)
			return False
		
	return [tokenList, tokenListInfo, linewiseTokenInfo]



####################################################################################################################
# This function takes two inputs.
# 1) inputLines - list of lines (strings), each delimited by a newline character (MUST)
# 2) inputList - list of tokens that we want to search in the tokenized version of the inputLines
# Output is a 5-item list, where each item is [tokenStartIndex,startLineNumber,startLineCharNumber,endLineNumber,endLineCharNumber]
# This means that we can find the inputList stream of tokens at the tokenStartIndex-th position in the tokenized version of the inputLines.
# Also, we can find it starting from inputLines[startLineNumber][startLineCharNumber] and ending at inputLines[endLineNumber][endLineCharNumber] 
####################################################################################################################
# TO-DO: If the inputList contains tokens ending with a newline, how is it to be handled (because inputLines does not capture end-of-line newlines)
# TO-DO: Not sure if the inputList tokens contain a quoted string literal, how it will be handled

def findTokenListInLines(inputLines, inputList):
#	global PRINT_DEBUG_MSG
#	PRINT_DEBUG_MSG = True
	
	# Take care of the special cases - the blank ones
	if (not inputList) and (not inputLines):
		return [0,0,0,0,0]
	elif not inputList and inputLines:	# Blank inputList but non-blank inputLines
		PRINT ("The inputList (matching pattern to be searched) is blank <",inputList,">" )
		return [0,-1,-1,-1,-1]
	elif not inputLines and inputList:	# Blank inputLines but non-blank inputList
		return [-1000000,-1,-1,-1,-1]
		
	# Check that inputLine is a list of Lines (strings ending with a newline). If it is a single string, make it a list
	if  isinstance(inputLines,list):
#		PRINT ("inputLines is indeed a list" )
		itemCount = 0
		while itemCount < len(inputLines):
			if not checkIfString(inputLines[itemCount]):
				PRINT ("Exiting - inside findTokenListInLines(inputLines, inputList), inputLines is not a list of proper strings - ", inputLines )
				return False
				sys.exit()
#			elif inputLines[itemCount][-1] != '\n':
#				PRINT ("Appending newline to the end of inputLines[",itemCount,"]" )
#				inputLines[itemCount] = inputLines[itemCount] + '\n'
			itemCount = itemCount + 1
#		PRINT ("inputLines is indeed a list of proper strings - ", inputLines )
	else:
#		PRINT ("inputLines is NOT a list" )
		if checkIfString(inputLines):
			if inputLines[-1] != '\n':
#				PRINT ("Appending newline to the end of inputLines" )
				inputLines = inputLines + '\n'
#			PRINT ("Converting the inputLines <",inputLines,">, which is a basic string but not a list, into a list" )
			inputLines = [inputLines]
#			PRINT ("Now the listified inputLines = ",inputLines )
		else:
			PRINT ("Unknown object type - inputLines = <",inputLines,"> - exiting" )
			PRINT ("Exiting - inside findTokenListInLines(inputLines, inputList), inputLines is Unknown object type - ", inputLines )
			return False
			sys.exit()
			
	# Check that inputList is a list of strings. If it is a single string, make it a list
	if  isinstance(inputList,list):
#		PRINT ("inputList is indeed a list" )
		for item in inputList:
			if not checkIfString(item):
				PRINT ("Exiting - inputList is not a list of proper strings - ", inputList )
				return False
				sys.exit()
			elif item != item.strip():
				PRINT (("inputList contains token <%s> that has whitespaces at their beginning or end - exiting"%item) )
				PRINT ("inputLines =",inputLines,"inputList =",inputList )
				return False
				sys.exit()
				
#		PRINT ("inputList is indeed a list of proper strings - ", inputList )
	else:
#		PRINT ("inputList is NOT a list" )
		if checkIfString(inputList):
#			PRINT ("Converting the inputList <",inputList,">, which is a basic string but not a list, into a list" )
			inputList = [inputList]
#			PRINT ("Now the listified inputList = ",inputList )
		else:
			PRINT ("Unknown object type - inputList = <",inputList,"> - exiting" )
			return False
			sys.exit()
	
	
	tokenizedLinesResult = tokenizeLines(inputLines)
	if tokenizedLinesResult == False:
		errorMessage = "ERROR in findTokenListInLines after calling tokenizeLines(inputLines)"
		errorRoutine(errorMessage)
		return False
	else:
		tokenizedLines = tokenizedLinesResult[0]
		
	PRINT ("tokenizedLines =",tokenizedLines)
	lineCharPositions = []	# For token #N in tokenizedLines, lineCharPositions[N] = [[startLineNum,startCharNum],[endLineNum,endCharNum]]

	# First find out the starting and ending <line,char> for each token
	tokenNum = 0
	tokenCharNum = 0
	matchingToken = False		# This tells if we are matching chars of a token, or matching whitespaces (if False)
	lastTokenMatched = False
	for lineNum in range(len(inputLines)):
		if lastTokenMatched:
			break
		for charNum in range(len(inputLines[lineNum])):
			if inputLines[lineNum][charNum]==tokenizedLines[tokenNum][tokenCharNum]:
				if tokenCharNum == 0:	# First char of the token matched
					start = [lineNum,charNum]
				if tokenCharNum == len(tokenizedLines[tokenNum])-1:	# Last char of the token matched
					end = [lineNum,charNum]
					lineCharPositions.append([start,end])
					if tokenNum == len(tokenizedLines)-1:
						lastTokenMatched = True
						break
					else:
						tokenNum += 1
						tokenCharNum = 0
				else:
					tokenCharNum += 1
			elif re.match("\s",inputLines[lineNum][charNum]):
				pass
			else:
				PRINT("For tokenNum =",tokenNum,", inputLines[",lineNum,"][",charNum,"] = ",inputLines[lineNum][charNum]," is non-whitespace, non-token char - should never happen")
				sys.exit()

	PRINT ("lineCharPositions =",lineCharPositions)

	# Next see if the inputList occurs as a substring of the tokenizedLines
	if len(tokenizedLines) < len(inputList):
		return [-1000000,-1,-1,-1,-1]
		
	matchStartIndex = -1000000	# Invalid value
	for i in range(len(tokenizedLines)-len(inputList)+1):
		if tokenizedLines[i] == inputList[0]:
			matchStartIndex = i
			mismatchFound = False
			for j in range(len(inputList)):
				if tokenizedLines[i+j] != inputList[j]:
					mismatchFound = True
					matchStartIndex = -1000000
					break
			if mismatchFound == False:
				PRINT ("inputList = ",inputList,"found starting at token #",matchStartIndex,"of tokenizedLines =",tokenizedLines)
				break
				
	if matchStartIndex < 0:
		PRINT ("Did not find any match :-(" )
		return [-1000000,-1,-1,-1,-1]
	else:
		returnValue = [matchStartIndex,lineCharPositions[matchStartIndex][0][0],lineCharPositions[matchStartIndex][0][1],lineCharPositions[matchStartIndex+len(inputList)-1][1][0],lineCharPositions[matchStartIndex+len(inputList)-1][1][1]]
		PRINT("Match found! returnValue =",returnValue)
		return returnValue
		

#inputLines = ['(a,b);\n', '\n', '\#define ADD_ONE(x) x+1']
#inputList = ['(', 'a', ',', 'b', ')']
		
#inputLines = ["b c","\n",'\n'," 	efgh \n", "a d"]
#inputList = ["c","efgh","a","a"]

#result1 = findTokenListInLines(inputLines, inputList)
#PRINT("result1 =",result1)
#PRINT("result2 =",result2)
#sys.exit()

####################################################################################################################
#  THE most important function. It takes in a tokenStream, and returns an AST
####################################################################################################################
def parseArithmeticExpression (arithmeticExpression):
#	PRINT ("arithmeticExpression to be parsed = ", arithmeticExpression )
#	PRINT ("len(arithmeticExpression) = ", len(arithmeticExpression) )
	
#	arithmeticExpressionNode = Node (arithmeticExpression, "arithmeticExpression")
#	parentNode.add_child(arithmeticExpressionNode)

	# Earlier this had a bug that if the input was a string instead of a list, it would break up string into individual chars
	if checkIfString(arithmeticExpression):
		return [arithmeticExpression]
	elif not isinstance(arithmeticExpression,list):
		errorMessage = "ERROR in parseArithmeticExpression: supplied input <%s> is neither a string nor a list"%(STR(arithmeticExpression))
		errorRoutine(errorMessage)
		return False

	global cDataTypes, cKeywords

	# The operator precedence table has the following format:
	# Rows at the beginning of this table (lower indices) have higher precedence over the later rows (higher indices).
	# Each row is a 2-member tuple. The first member is a set of the operators with equal precedence.
	# The second member indicates which operand(s) the Operator takes, and in what order. This tells if it is Left-to-Right associative, or Right-to-Left.
	# +1 means the operand lies to the operator's right (naturally, -1 means to the left)
	operatorPrecedence = [ 	[['##'],[-1,+1]],						# Left-to-Right (presumably), Concatenate	# TO-DO fix the associativity
#							[['++','--','()','[]','.','->'],[-1]],	# Left-to-Right, postfix increment/decrement
							[['++','--','()','[]'],[-1]],			# Left-to-Right, postfix increment/decrement
							[['.','->'],[-1,+1]],					# Left-to-Right, struct member assignment
							[['++','--','+','-','!','~','(typecast)','*','&','sizeof','_Alignof'],[+1]],	#Right-to-Left, prefix increment/decrement, unary +-
							[['/','*','%'],[-1,+1]],				# Left-to-Right
							[['-','+'],[-1,+1]],					# Left-to-Right, Addition and subtraction
							[['<<','>>'],[-1,+1]],					# Left-to-Right, Bitwise left/right shift operators
							[['<','<=','>','>='],[-1,+1]],			# Left-to-Right, relational
							[['==','!='],[-1,+1]],					# Left-to-Right, relational
							[['&'],[-1,+1]],						# Left-to-Right, bitwise AND
							[['^'],[-1,+1]],						# Left-to-Right, bitwise XOR
							[['|'],[-1,+1]],						# Left-to-Right, bitwise OR
							[['&&'],[-1,+1]],						# Left-to-Right, logical AND
							[['||'],[-1,+1]],						# Left-to-Right, logical OR
							[['?'],[+3,+1,-1]],						# Right-to-Left, Ternary conditional ?:
							[['=','+=','-=','*=','/=','%=','<<=','>>=','&=','^=','|='],[+1,-1]], # Right-to-Left, Assignments
							[[','],[-1,+1]]]						# Left-to-Right, comma

	operatorSet = []
	i=0
	while i<len(operatorPrecedence):
		operatorSet = operatorSet + operatorPrecedence[i][0]
		i += 1
	operatorSet = operatorSet + [':']	# Need to add it separately since it does not get covered automatically
#	PRINT ("operatorSet = ", operatorSet )

# Not sure why we are doing this
	if len(arithmeticExpression) < 1:		# Question: Why is this?
		return arithmeticExpression
	elif len(arithmeticExpression) == 1 and arithmeticExpression[0] not in cDataTypes: #Question: Why only cDataTypes, instead of cDataTypes+cKeywords?
		return arithmeticExpression

	
	# We try to "condense" the multiple consecutive elements of the arithmeticExpression list into one, thereby reducing the list size
	operatorOperandArray = []
	i=0
	while i < len(arithmeticExpression):
	
		# Handle the case that the expression is a datatype
#		PRINT ("Input arithmeticExpression = ", arithmeticExpression )
#		PRINT ("Currently handling arithmeticExpression[",i,"] =", arithmeticExpression[i] )
		if arithmeticExpression[i] in cDataTypes:
#			PRINT ("\n\n\n\n\n\n\narithmeticExpression[i] in cDataTypes:\n\n\n\n\n\n" )
			dataTypeIndex = i+1
#			PRINT ("dataTypeIndex = ", dataTypeIndex )
			# We might have data type consisting of multiple words, like unsigned short int 
			# We need to handle the pointer ("*") and array ("[]") later, and recall that we can have array[arithmeticExpression] type also
			while dataTypeIndex <len(arithmeticExpression) and arithmeticExpression[dataTypeIndex] in cDataTypes:
				dataTypeIndex += 1
#			PRINT ("Last dataTypeIndex = ", dataTypeIndex )
			newDataTypeToken = ["datatype",arithmeticExpression[i:dataTypeIndex]]
			operatorOperandArray.append(newDataTypeToken)
			i=dataTypeIndex-1
			
		# Handle parenthesized expressions: Strip the braces, and put them as a single list item
		elif arithmeticExpression[i] == "(":
			if matchingBraceDistance(arithmeticExpression[i:]) < 1:
				PRINT ("ERROR - no matching brace for ",arithmeticExpression[i]," ... exiting" )
				return False
				sys.exit()
			j= i + matchingBraceDistance(arithmeticExpression[i:])
			# There could be multiple cases: Simple braces, function call (including sizeof), and typecasting
			#Function call (including sizeof)
#			if i>0 and arithmeticExpression[i-1] not in removeItemsIn2ndListFrom1st(cKeywords, ["sizeof"]) and arithmeticExpression[i-1] not in operatorSet:
			if operatorOperandArray and operatorOperandArray[-1] not in cKeywords and operatorOperandArray[-1] not in operatorSet: # Function call
#				PRINT ("Found function call\n" )
				functionName = operatorOperandArray[-1]
				del operatorOperandArray[-1]
				parseArithmeticExpressionOutput = parseArithmeticExpression(arithmeticExpression[i+1:j])
				if parseArithmeticExpressionOutput == False:
					PRINT ("ERROR after calling parseArithmeticExpression(arithmeticExpression[i+1:j]) for arithmeticExpression[",i,"+1:",j,"] = ",arithmeticExpression[i+1:j] )
					return False
					sys.exit()
				operatorOperandArray.append(["function()", functionName, ["()",parseArithmeticExpressionOutput]])
				i = j
			# The arithmeticExpression[j] is the ending brace for the typecasting type. The variable being typecast will start from j+1
			elif j+1<len(arithmeticExpression) and arithmeticExpression[j+1] not in cKeywords and arithmeticExpression[j+1] not in operatorSet:
				PRINT ("Found typecasting\n" )
				#The next token to be typecast is either a variable or yet another parenthesized expression
				typecastVarEndIndex = j+1
				if arithmeticExpression[j+1] == "(":	#yet another parenthesized expression
					if matchingBraceDistance(arithmeticExpression[j+1:]) < 1:
						PRINT ("ERROR - no matching brace for ",arithmeticExpression[j+1]," ... exiting" )
						return False
						sys.exit()
					typecastVarEndIndex = j+1 + matchingBraceDistance(arithmeticExpression[j+1:])
				parseArithmeticExpressionOutput1 = parseArithmeticExpression (arithmeticExpression[i+1:j])
				parseArithmeticExpressionOutput2 = parseArithmeticExpression(arithmeticExpression[j+1:typecastVarEndIndex+1])
				if parseArithmeticExpressionOutput1 == False:
					PRINT ("ERROR after calling parseArithmeticExpression (arithmeticExpression[i+1:j]) for arithmeticExpression[",i,"+1:",j,"] =",arithmeticExpression[i+1:j] )
					return False
				elif parseArithmeticExpressionOutput2 == False:
					PRINT ("ERROR after calling parseArithmeticExpression(arithmeticExpression[j+1:typecastVarEndIndex+1]) for arithmeticExpression[",j,"+1:",typecastVarEndIndex,"+1] =",arithmeticExpression[j+1:typecastVarEndIndex+1] )
					return False
				newTypecastToken = ["typecast",["()",parseArithmeticExpressionOutput1], parseArithmeticExpressionOutput2]
				operatorOperandArray.append(newTypecastToken)
				i = typecastVarEndIndex
			else:
				parseArithmeticExpressionOutput = parseArithmeticExpression(arithmeticExpression[i+1:j])
				if parseArithmeticExpressionOutput == False:
					PRINT ("ERROR after calling parseArithmeticExpression(arithmeticExpression[i+1:j]) for arithmeticExpression[",i,"+1:",j,"] = ", arithmeticExpression[i+1:j] )
					return False
				operatorOperandArray.append(["()", parseArithmeticExpressionOutput])
				i = j
		# Handle parenthesized expressions: Strip the braces, and put them as a single list item
		elif arithmeticExpression[i] == "{" :
			if matchingBraceDistance(arithmeticExpression[i:]) < 1:
				PRINT ("ERROR - no matching brace for ",arithmeticExpression[i]," ... exiting" )
				return False
				sys.exit()
			j= i + matchingBraceDistance(arithmeticExpression[i:])
			parseArithmeticExpressionOutput = parseArithmeticExpression(arithmeticExpression[i+1:j])
			if parseArithmeticExpressionOutput == False:
				PRINT ("ERROR after calling parseArithmeticExpression(arithmeticExpression[i+1:j]) for arithmeticExpression[",i,"+1:",j,"] = ",arithmeticExpression[i+1:j] )
				return False
			operatorOperandArray.append(["{}", parseArithmeticExpressionOutput])
			i = j
		elif arithmeticExpression[i] == "[" :
			if matchingBraceDistance(arithmeticExpression[i:]) < 1:
				PRINT ("ERROR - no matching brace for ",arithmeticExpression[i]," ... exiting" )
				return False
				sys.exit()
			j= i + matchingBraceDistance(arithmeticExpression[i:])
			parseArithmeticExpressionOutput = parseArithmeticExpression(arithmeticExpression[i+1:j])
			if parseArithmeticExpressionOutput == False:
				PRINT ("ERROR after calling parseArithmeticExpression(arithmeticExpression[i+1:j]) for arithmeticExpression[",i,"+1:",j,"] =",arithmeticExpression[i+1:j] )
				return False
			operatorOperandArray.append(["[]", parseArithmeticExpressionOutput])
			i = j
		else:
#			PRINT ("Adding arithmeticExpression[",i,"] = ", arithmeticExpression[i] )
			operatorOperandArray.append(arithmeticExpression[i])
		i += 1

	#Check if operatorOperandArray has a single member, and that itself is a list. If it is, then return that single member
	if len(operatorOperandArray)==1 and isinstance(operatorOperandArray[0],list):
		operatorOperandArray = operatorOperandArray[0]
		
#	PRINT ("\nIncoming arithmeticExpression = <", arithmeticExpression, ">\nAfter handling the parenthesization, function call, it translates into" )
#	PRINT ("operatorOperandArray = ", operatorOperandArray, "\nNow we will apply the operator precedence and condense this even further." )
	
	while True: 
#		PRINT ("\n\noperatorOperandArray[]", operatorOperandArray, "currently has",len(operatorOperandArray),"members" )
		operatorOperandArrayOrigLen = len(operatorOperandArray)
		if len(operatorOperandArray) <= 1:
#			PRINT ("\n\n\n\n\n" )
			break
		newToken = []
		operatorAppliedToOperand = False
		# Look for the highest-precedence available operator
		for j in range(len(operatorPrecedence)):
			if operatorAppliedToOperand:
				break
			for k in range(len(operatorPrecedence[j][0])):
				if operatorAppliedToOperand:
					break
				for x in range(len(operatorOperandArray)):
					# For Left-to-Right (or Right-to-Left) associativity we scan accordingly
					if operatorPrecedence[j][1][0] >= +1:
#						PRINT ("Special case for Right-to-Left associativity" )
						i = len(operatorOperandArray)-1-x
#						PRINT ("i=",i,"x=",x,"len(operatorOperandArray)=",len(operatorOperandArray),"operatorOperandArray=",operatorOperandArray )
					else:
						i = x
					if operatorAppliedToOperand:
						break
					if operatorPrecedence[j][0][k] == operatorOperandArray[i]:
						hasValidOperands = True
						for operandOffset in range(len(operatorPrecedence[j][1])):
							# Ensure that the operator currently has sufficient operands
							if ((i+operatorPrecedence[j][1][operandOffset] >= len(operatorOperandArray)) or 
							    (i+operatorPrecedence[j][1][operandOffset] <0) or 
							    (operatorOperandArray[i+operatorPrecedence[j][1][operandOffset]] in operatorSet)):
								hasValidOperands = False
								PRINT ("hasValidOperands =",hasValidOperands,"for",operatorPrecedence[j][1] )
						# Special rules for operators that can be interpreted as either unary or binary. 
						if hasValidOperands and operatorOperandArray[i] in ("+","-","*","&") and i>0 and len(operatorPrecedence[j][1])==1 and operatorOperandArray[i-1] not in operatorSet:
							hasValidOperands = False
						# Also handle the ternary operator
						elif hasValidOperands and operatorOperandArray[i] == "?" and operatorOperandArray[i+2] != ":":
							hasValidOperands = False
						
						if hasValidOperands:
							operatorAppliedToOperand = True
							minIndex = i + min(0,min(operatorPrecedence[j][1]))
							maxIndex = i + max(0,max(operatorPrecedence[j][1]))
#							PRINT ("x =",x, "i =",i,"j =",j,"k =",k, "operator =",operatorPrecedence[j][0][k], "minIndex = ", minIndex, "maxIndex = ", maxIndex,"operatorOperandArray[minIndex:maxIndex+1]=",operatorOperandArray[minIndex:maxIndex+1] )
							newToken = operatorOperandArray[minIndex:maxIndex+1]
#							PRINT ("deleting newToken =",newToken, "starting at index", minIndex,"and ending before index", maxIndex+1 )
							del operatorOperandArray[minIndex:maxIndex+1]
#							PRINT ("After deleting, operatorOperandArray = ",operatorOperandArray )
							operatorOperandArray.insert(minIndex,newToken)
#							PRINT ("After inserting",newToken, "\noperatorOperandArray = ",operatorOperandArray,"\n" )
							break
		if operatorOperandArrayOrigLen < len(operatorOperandArray):
			PRINT ("The numbe of operands should not increase - exiting!!!\n\n\n" )
			PRINT ("operatorOperandArrayOrigLen =",operatorOperandArrayOrigLen,"operatorOperandArray =",operatorOperandArray )
			return False
			sys.exit()
		elif operatorOperandArrayOrigLen == len(operatorOperandArray):
#			PRINT ("No longer able to apply the operators - exiting the loop!!!\n\n\n" )
			break
			
	#Check if operatorOperandArray has a single member, and that itself is a list. If it is, then return that single member
	if len(operatorOperandArray)==1 and isinstance(operatorOperandArray[0],list):
#		PRINT ("Single-member List, hence returning operatorOperandArray[0]=",operatorOperandArray[0] )
		return operatorOperandArray[0]
	else:
#		PRINT ("multi-member List, hence returning operatorOperandArray =",operatorOperandArray )
		return operatorOperandArray


'''
###############################################
# Testing if the evaluation realy works
###############################################
from random import seed
from random import randint
from random import random
seed(10)
for _ in range(0,1000):
	exprList = []
	exprStr = ""
	for _ in range(10):
		valueInt = randint(0,10)
		valueFloat = random()
#		print valueInt, valueFloat
		exprList.append(str(valueInt))
		exprStr+=(str(valueInt))
		exprList.append("+" if valueFloat < 0.5 else "-")
		exprStr+=("+" if valueFloat < 0.5 else "-")
	exprList.append("0")
	exprStr+="0"
	print "exprStr =",exprStr,"eval(",exprStr,") =",eval(exprStr)
	result = evaluateArithmeticExpression(parseArithmeticExpression(exprList))
	print exprList,"=",exprList,"evaluates to",result[1]
	final = ("SUCCESS" if result[1] == eval(exprStr) else "FAIL")
	if final == "FAIL":
		print "ERROR"
		sys.exit()
sys.exit()
'''

########################################################################################################################################################
# This function takes in an input STRING (which is NOT a list) containing an address/size in human-readable formats, and returns the decimal equivalent
# For example, inputString = "1GB+5MB-384KB" will yeild [True, 1078591488]. Recall that we cannot send just False in case of an error 
# because False (equivalent of 0) is a valid return value.
########################################################################################################################################################
def convertByteUnits2Decimal(inputString):

	dicSize = {"KB":"*(1<<10)","MB":"*(1<<20)","GB":"*(1<<30)","TB":"*(1<<40)","PB":"*(1<<50)","EB":"*(1<<60)","ZB":"*(1<<70)","YB":"*(1<<80)"}
	
	if not checkIfString(inputString):
		return [False,None]
		
#	PRINT (dicSize)
	convertedString = inputString
	for key,value in dicSize.items():
#		PRINT ("Replaceing all occurrences of ",key,"with",value,"in convertedString =",convertedString)
		convertedString = convertedString.replace(key,value)
	PRINT ("convertedString =",convertedString)
	
	tokenizeLinesResult = tokenizeLines(convertedString)
	if tokenizeLinesResult == False:
		errorMessage = "ERROR in convertByteUnits2Decimal() tokenizing <%s>"%convertedString
		errorRoutine(errorMessage)
		return [False,None]
	else:
		tokenizeLinesResult = tokenizeLinesResult[0]
	
	parseArithmeticExpressionResult = parseArithmeticExpression(tokenizeLinesResult)
	if parseArithmeticExpressionResult == False:
		errorMessage = "ERROR in convertByteUnits2Decimal() parsing <%s>"%tokenizeLinesResult
		errorRoutine(errorMessage)
		return [False,None]
		
	evaluateArithmeticExpressionResult = evaluateArithmeticExpression(parseArithmeticExpressionResult)
	if evaluateArithmeticExpressionResult[0] == False:
		errorMessage = "ERROR in convertByteUnits2Decimal() evaluating <%s>"%evaluateArithmeticExpressionResult
		errorRoutine(errorMessage)
		return [False,None]
		
	num = evaluateArithmeticExpressionResult[1]
	PRINT ("Result = ",num)
	if isinstance(num,float):
		result = int(num + 0.01)	# A hack to cover the case when the number is actual very near to an integral value, but just LESS than that value. So, we give it a bit of a push
	else:
		result = num
	return [True, result]

#inputString = "1KB/33"
#print convertByteUnits2Decimal(inputString)
#sys.exit()

############################################################################################
# Given an AST (this NOT a tokenstream), this method outputs the corresponding string
############################################################################################
def outputTextArithmeticExpressionFromAST (arithmeticExpressionAST):
	global cDataTypes
#	PRINT ("\n\nIncoming already-listified AST string = ", arithmeticExpressionAST )
	if checkIfString(arithmeticExpressionAST):
#		PRINT ("It's a string - returning as it is!" )
		return arithmeticExpressionAST
	elif isinstance(arithmeticExpressionAST,list):
		# If it is a list of lists, but contains only a single member, remove one level of listification
		if len(arithmeticExpressionAST) == 1:
#			PRINT ("Returning",arithmeticExpressionAST[0] )
			return outputTextArithmeticExpressionFromAST (arithmeticExpressionAST[0])
		else:	
			if not isASTvalid(arithmeticExpressionAST):
				PRINT ("\nWARNING - outputting Text from arithmeticExpressionAST may not work because the inputList is not a valid AST\n" )

			outputString = ""
			i = 0
			while i < len(arithmeticExpressionAST):
#				PRINT ("\nhandling arithmeticExpressionAST[",i,"] =", arithmeticExpressionAST[i], "outputString = <%s>"% outputString )
				if i==0 and (arithmeticExpressionAST[i] == "()" or arithmeticExpressionAST[i] == "{}" or arithmeticExpressionAST[i] == "[]" or arithmeticExpressionAST[i] == "<>" ): 
#					PRINT ("Found", arithmeticExpressionAST[i], "for i =",i )
					if len(arithmeticExpressionAST) == 2:
						outputTextArithmeticExpressionFromASTOutput = outputTextArithmeticExpressionFromAST(arithmeticExpressionAST[i+1])
						if outputTextArithmeticExpressionFromASTOutput == False:
							PRINT ("Inside outputTextArithmeticExpressionFromAST, error after calling outputTextArithmeticExpressionFromAST(arithmeticExpressionAST[i+1]) for arithmeticExpressionAST[",i,"+1] =",arithmeticExpressionAST[i+1] )
							return False
						else:
							outputString += arithmeticExpressionAST[i][0]+ ' ' + outputTextArithmeticExpressionFromASTOutput + ' ' + arithmeticExpressionAST[i][1]
					else:
						PRINT ("Inside outputTextArithmeticExpressionFromAST, unknown tokens for",arithmeticExpressionAST[i] )
						return False
						sys.exit()
					i += 1	# We are eating up one extra token
				elif i==0 and arithmeticExpressionAST[0]=="function()": 
					if len(arithmeticExpressionAST)!=3:
						PRINT ("Inside outputTextArithmeticExpressionFromAST, invalid function call",arithmeticExpressionAST )
						return False
						sys.exit()
					else:
						outputTextArithmeticExpressionFromASTOutput = outputTextArithmeticExpressionFromAST(arithmeticExpressionAST[2])
						if outputTextArithmeticExpressionFromASTOutput == False:
							PRINT ("Error after calling outputTextArithmeticExpressionFromAST(arithmeticExpressionAST[2]) for arithmeticExpressionAST[2] =",arithmeticExpressionAST[2] )
							return False
						else:
							outputString += arithmeticExpressionAST[1]+ ' ' + outputTextArithmeticExpressionFromASTOutput
							i += 2 # We are eating up two extra tokens
				elif i==0 and arithmeticExpressionAST[0]=="datatype": 
					if len(arithmeticExpressionAST)!=2:
						PRINT ("Inside outputTextArithmeticExpressionFromAST, invalid datatype expression",arithmeticExpressionAST )
						return False
						sys.exit()
					else:
						for item in arithmeticExpressionAST[1]:
							if item not in cDataTypes:
								PRINT ("Inside outputTextArithmeticExpressionFromAST, item", item,"in arithmeticExpressionAST[1] = ",arithmeticExpressionAST[1], "doesn't belong to cDataTypes =",cDataTypes )
								return False
								sys.exit()
						outputString +=  ' ' + ' '.join(arithmeticExpressionAST[1])
						i += 2 # We are eating up two extra tokens
					
				else:
					outputTextArithmeticExpressionFromASTOutput = outputTextArithmeticExpressionFromAST(arithmeticExpressionAST[i])
					if outputTextArithmeticExpressionFromASTOutput == False:
						PRINT ("ERROR after calling outputTextArithmeticExpressionFromAST(arithmeticExpressionAST[i]) for arithmeticExpressionAST[",i,"] =",arithmeticExpressionAST[i] )
						return False
					else:
#						PRINT ("found no () for i=",i )
						outputString +=  ' ' + outputTextArithmeticExpressionFromAST(arithmeticExpressionAST[i])
#				PRINT ("After completion of loop for i=",i,"outputString =", "outputString = <%s>"% outputString )
				i += 1
			
			outputString = outputString.strip()
			
			# Cross-verify that we indeed got the right string that would have yielded the same arithmeticExpressionAST
			tokenizeLinesOutput = tokenizeLines(outputString)
			if tokenizeLinesOutput == False:
				PRINT ("ERROR in outputTextArithmeticExpressionFromAST after calling tokenizeLines(outputString) for outputString = ", outputString )
				return False
			else:
				tokenizeLinesOutput = tokenizeLinesOutput[0]
				
			outputStringTokenizedAndParsed = parseArithmeticExpression(tokenizeLinesOutput)
			if outputStringTokenizedAndParsed == False:
				PRINT ("ERROR after calling parseArithmeticExpression(tokenizeLinesOutput) for tokenizeLinesOutput =",tokenizeLinesOutput )
				return False
				sys.exit()
			lhsAST = removeUnnecessaryListification(arithmeticExpressionAST)
			rhsAST = removeUnnecessaryListification(outputStringTokenizedAndParsed)
			if lhsAST != rhsAST:
				# Why this is a warning and not an error is the following. For example, suppose the input AST is ['a','+',[['b','-','c'],'*','d']]. 
				# This AST  will yield a+b-c*d, not a+(b-c)*d because the parenthesization is missing in the input AST. 
				# In other words, the Tokenstream-->Text transformation is losing information that we can never get back.
				# Now, if we tokenize and parse a+b-c*d, we will get ['a','+',['b','-',['c','*','d']]], which is different from ['a','+',[['b','-','c'],'*','d']].
				PRINT ("WARNING - somehow the outputString <",outputString,">\nwhich tokenizes/parses into <",outputStringTokenizedAndParsed,">\ndoesn't match the arithmeticExpressionAST <",arithmeticExpressionAST,"> - exiting" )
				PRINT ("lhsAST = ",lhsAST, "\nrhsAST = ",rhsAST )
#				sys.exit()

			return outputString

	else:
		PRINT ("\n\nERROR inside outputTextArithmeticExpressionFromAST - unknown passed object type", type(arithmeticExpressionAST) )
		return False
		sys.exit()


#str = "2+3+func(c+d)*(n)"
#strTokenized = tokenizeLines(str)
#strAST = parseArithmeticExpression(strTokenized)
#strAST = ['a','+',[['b','-','c'],'*','d']]
#strASTtextified = outputTextArithmeticExpressionFromAST (strAST)
#PRINT ("strASTtextified = ",strASTtextified )
#PRINT ("\nThe Original str=<%s>, \nstrTokenized=<%s>, \nstrAST=<%s>, \nstrASTtextified =<%s>"%(str,strTokenized,strAST,strASTtextified) )
#sys.exit()

##################################################################################################################################################################################
# This function returns a tuple of <success/failure, count>. We cannot return a single thing because 0 is same as False in Python, and 0 is a valid return value for this routine
# This function will count ALL the combined occurrences of the same item as only ONE occurrence, and count it only once.
# So, essentially it returns how many of those itemsToCheck actually occur in the inputList
##################################################################################################################################################################################
def totalOccurrenceCount(inputList, itemsToCheck):
	if not inputList:
		errorMessage = "Blank inputList to totalOccurrenceCount()"
		errorRoutine(errorMessage)
		return [False,0]
	elif not isinstance(inputList, list):
		errorMessage = "ERROR - Unknown input object to totalOccurrenceCount() " + STR(inputList) + " - exiting"
		errorRoutine(errorMessage)
		return [False,0]
	elif not itemsToCheck:
		errorMessage = "Blank itemsToCheck to totalOccurrenceCount()"
		errorRoutine(errorMessage)
		return [False,0]
	elif not isinstance(itemsToCheck, list):
		errorMessage = "ERROR - Unknown input object to totalOccurrenceCount() " + STR(itemsToCheck) + " - exiting"
		errorRoutine(errorMessage)
		return [False,0]

	returnStatus = True
	returnCount = 0
	
	for item in itemsToCheck:
		itemCount = 0
		for listItem in inputList:
			if item == listItem:
				itemCount += 1
		if itemCount > 0:
			returnCount += 1
			if itemCount > 1:
				errorMessage = "WARNING: Duplicate "+ STR(item)
				errorRoutine(errorMessage)
				returnStatus = False
	
	return [returnStatus,returnCount]

def noConflictingOccurrences(inputList, itemsToCheck):
	returnStatus = totalOccurrenceCount(inputList, itemsToCheck)
	if returnStatus[0] == False:
		return False
	elif returnStatus[0] == True:
		occurrenceCount = returnStatus[1]
		if occurrenceCount > 1:
			errorMessage = "ERROR: We cannot have conflicting "+ STR(itemsToCheck) +  " in < " + STR(inputList) + " >"
			errorRoutine(errorMessage)
			return False
	return True

#######################################################################################################################################################
# This function takes a list of tokens representing a fragment of single variable declaration statement. It returns a list of two items:
# 1. True / False, depending on whether the syntax is correct or not
# 2. Yet another dictionary. This list will have the following key-values: 
#    a. ["distance"] - the "distance" of of the last token (which should be a ")" - the 2nd one) within this __attribute_(( attributes )) statement 
#       from the first "(" right after the __attribute__ token.
#        Only this key-value pair is mandatory within the dictionary. Rest all are optional
#    b. ["packed"] - should be True, if there
#    c. ["aligned"] - should be a value that is a proper two's power
#######################################################################################################################################################
def parseAttribute(inputList, i=0):
	PRINT ("Inside parseAttribute(inputList=<",inputList,">, i=",i)
	if not inputList:
		OUTPUT ("Blank input to parseAttribute()" )
		errorMessage = "Blank input to parseAttribute()"
		errorRoutine(errorMessage)
		return [False, None]
	elif not isinstance(inputList,list):
		errorMessage = "Input to parseAttribute() is not a list"
		errorRoutine(errorMessage)
		return [False, None]
	elif inputList[i:i+3] != [ATTRIBUTE_STRING,"(","("]:
		errorMessage = "Input to parseAttribute() does not have __attribute__ at index %d - inputList[%d:%d+3] =%s"%(i,i,i,STR(inputList[i:i+3]))
		errorRoutine(errorMessage)
		return [False, None]

	lastIndexToDisplay = i+inputList[i:].index(";") if ";" in inputList[i:] else len(inputList)

	d = matchingBraceDistance(inputList[i+1:])
	
	if d <1 or inputList[i+1+d] != ")" or inputList[i+1+d-1] != ")":
		OUTPUT ("i =",i,"d =",d, "inputList =", inputList[i:lastIndexToDisplay+1])
		errorMessage = "ERROR in parseAttribute() - no matching \"))\" following the __attribute__(( %s"%STR(inputList[i+1:i+1+d+1])
		errorRoutine(errorMessage)
		return [False, None]
	else:
		attributes = {"distance":d}
#		parenthesizedArguments = inputList[i+2:i+1+d]
		
		arguments = inputList[i+3:i+d]
		PRINT ("Going to parse arguments =",arguments)
		
		k = 0
		while (k < len(arguments)):
			PRINT("Currently handling __attribute__((",arguments[k],"))")
			if arguments[k] in (",",")"):
				k += 1
			elif arguments[k] in ("packed","__packed__"):
				attributes[PACKED_STRING] = True
				k += 1
			elif arguments[k] in ("aligned","__aligned__"):
				if k == len(arguments)-1 or arguments[k+1] in (")",",","packed","__packed__"):		# TO-DO: Need to put other keywords here
					attributes[ALIGNED_STRING] = ALIGNED_DEFAULT_VALUE
					k += 1
				elif arguments[k+1] != "(" or ")" not in arguments[k+2:]:
					errorMessage = "ERROR in parseAttribute() - aligned(%s) is not valid"%(STR(arguments[k+1]))
					errorRoutine(errorMessage)
					return [False,attributes]
				else:
					distance = matchingBraceDistance(arguments[k+1:])
					if distance < 1:
						errorMessage = "ERROR in parseAttribute() - aligned(%s) is not valid due to no end brace"%(STR(arguments[k+1:]))
						errorRoutine(errorMessage)
						return [False,attributes]
					else:
						item = arguments[k+2:k+1+distance]
						PRINT("Currently going to resolve the item=",item)
						parseArithmeticExpressionResult = parseArithmeticExpression(item)
						if parseArithmeticExpressionResult == False:
							errorMessage = "ERROR in parseAttribute() - error calling parseArithmeticExpression(parenthesized alignment value of = <%s> "%(STR(item), STR(parseArithmeticExpressionResult))
							errorRoutine(errorMessage)
							return [False,attributes]
						else:
							evaluateArithmeticExpressionResult = evaluateArithmeticExpression(parseArithmeticExpressionResult)
							if evaluateArithmeticExpressionResult[0] != True:
								errorMessage = "ERROR in parseAttribute() - error calling evaluateArithmeticExpression(AST = <%s>) after an aligned statement"%(STR(parseArithmeticExpressionResult))
								errorRoutine(errorMessage)
								return [False,attributes]
							else:
								result = evaluateArithmeticExpressionResult[1]
								if not checkIfIntegral(result) or result <1:
									errorMessage = "ERROR in parseAttribute() - output (%s) from evaluateArithmeticExpression() after a __attribute__((aligned)) statement is not integral or <1"%(STR(result))
									errorRoutine(errorMessage)
									return [False,attributes]
								elif result & (result-1) != 0:	# check that it is proper power of 2
									errorMessage = "ERROR in parseAttribute() - output (%s) from evaluateArithmeticExpression() after a __attribute__((aligned)) statement must be a power of 2"%(STR(result))
									errorRoutine(errorMessage)
									return [False,attributes]
								elif ALIGNED_STRING in getDictKeyList(attributes):
									attributes[ALIGNED_STRING] = max(result,attributes[ALIGNED_STRING])
									PRINT("Assigned the result =",result,"to the aligned, while the content of current pragmaPackStack is",pragmaPackStack)
									k = k+1+distance
								else:
									attributes[ALIGNED_STRING] = result
									PRINT("Assigned the result =",result,"to the aligned, while the content of current pragmaPackStack is",pragmaPackStack)
									k = k+1+distance
			else:
				errorMessage = "ERROR in parseAttribute() - unsupported arguments[k=%d] in __aligned__ ((%s))"%(k,STR(arguments[k]))
				errorRoutine(errorMessage)
				return [False,attributes]
				
				
		PRINT ("For the inputList = <", flattenList(inputList[i:i+1+d+1]),"> Returning attributes =",attributes)
		return [True,attributes]
								



	
#######################################################################################################################################################
# This function takes a list of tokens representing a single variable declaration statement, and returns the index where its type specifier ends;
# Basically, the very next token should be either the "*", "(" or the variable identifier itself.
# For example, for this statement <singed long int i;>, it will return 2
#######################################################################################################################################################
def findTypeSpecifierEndIndex(inputList):

	typeSpecifierEndIndex = -1000		# Invalid value. We cannot return False, since False is same as 0 in Python, and 0 is valid return value.
	if not inputList:
		PRINT ("Blank input to findTypeSpecifierEndIndex()" )
		return typeSpecifierEndIndex
	elif not isinstance(inputList,list):
		PRINT ("ERROR - Unknown input object to findTypeSpecifierEndIndex()", inputList," - exiting" )
		return typeSpecifierEndIndex

	baseTypeSpecifier = ['void','char','short','int','long','float','double', 'long long']
	typeSpecifierImplicit = ['signed','unsigned']     # TO-DO: need to add <struct-or-union-specifier> <enum-specifier> <typedef-name>
#	storageClassSpecifier = [ 'auto','register','static','extern','typedef']	#just keep them here to tell you what they are
#	typeQualifier = ['const','volatile']										#just keep them here to tell you what they are
	
	#TO-DO: add the typedefs too
	derivedTypeSpecifier = []
	if typedefs:
		derivedTypeSpecifier.extend(getDictKeyList(typedefs))

#	if typedefsBuiltin:
#		derivedTypeSpecifier.extend(getDictKeyList(typedefsBuiltin))
		
	# Currently not using, since this list will be changing dynamically
	typeSpecifier = listDeepCopy(baseTypeSpecifier)
	if derivedTypeSpecifier:
		typeSpecifier.extend(derivedTypeSpecifier[:])

	# We take a rather conservative approach in parsing the __attribute__ statements. You see, there can be multiple __attribute__ statements inside a single
	# variable declaration, and they can appear at a number of places.
	i = 0
	while i<len(inputList):
		if inputList[i] == ATTRIBUTE_STRING:
			parseAttributeResult = parseAttribute(inputList[i:])
			if parseAttributeResult[0] != True:
				errorMessage = "ERROR in findTypeSpecifierEndIndex() after calling parseAttribute()"
				errorRoutine(errorMessage)
				return typeSpecifierEndIndex
			else:
				d = parseAttributeResult[1]["distance"]
				typeSpecifierEndIndex = i+1+d
				i = typeSpecifierEndIndex
		# TO-DO - to add the other qualifiers with the struct/union declaration
		elif inputList[i] == "enum":
			if inputList[i+1] not in getDictKeyList(enums):
				OUTPUT ("ERROR in findTypeSpecifierEndIndex() - enum", inputList[i+1]," has no previous declaration - exiting" )
				return typeSpecifierEndIndex
			else:
				typeSpecifierEndIndex = i+1
				i = typeSpecifierEndIndex
		elif inputList[i] == "struct" or inputList[i] == "union":
			lastItemConsumedIndex = i
			# There might be multiple __attribute__ statements right after the struct/union keyword
			while inputList[lastItemConsumedIndex+1] == ATTRIBUTE_STRING:
				parseAttributeResult = parseAttribute(inputList[lastItemConsumedIndex+1:])
				if parseAttributeResult[0] != True:
					errorMessage = "ERROR in findTypeSpecifierEndIndex() after calling parseAttribute()"
					errorRoutine(errorMessage)
					return typeSpecifierEndIndex
				else:
					d = parseAttributeResult[1]["distance"]	# Distance of the last brace from the first brace within the __attribute__ (( ...  )) statement
#					lastItemConsumedIndex = lastItemConsumedIndex+1+d		# Possible bug????
					lastItemConsumedIndex = lastItemConsumedIndex+1+d+1
			if inputList[lastItemConsumedIndex+1] != "{":
				lastItemConsumedIndex = lastItemConsumedIndex + 1
				structName = inputList[lastItemConsumedIndex]
				structOrUnionType = inputList[i]
				if inputList[lastItemConsumedIndex] not in getDictKeyList(structuresAndUnionsDictionary):
					PRINT ("ERROR: in findTypeSpecifierEndIndex() - struct", inputList[lastItemConsumedIndex+1]," has no previous declaration - hopefully it will be declared later" )
					PRINT ("Adding the empty declaration of struct",structName," to the structuresAndUnionsDictionary dictionary")
					structuresAndUnionsDictionary[structName] = {"type":structOrUnionType}
					structuresAndUnionsDictionary[structName]["parentStructName"] = "--Global--"
					structuresAndUnionsDictionary[structName]["components"] = []
			typeSpecifierEndIndex = lastItemConsumedIndex
			i = typeSpecifierEndIndex
		elif ((inputList[i] in baseTypeSpecifier) or (inputList[i] in derivedTypeSpecifier) or (inputList[i] in typeSpecifierImplicit) 
			or (inputList[i] in storageClassSpecifier) or (inputList[i] in typeQualifier) or (inputList[i] in getDictKeyList(typedefs))) :
			typeSpecifierEndIndex = i
		else:
			break
		i = i+1
		
	PRINT ("From findTypeSpecifierEndIndex(), returning return value of ",typeSpecifierEndIndex,"for inputList =",STR(inputList) )
	return typeSpecifierEndIndex

#######################################################################################################################################################
#This function takes a list of tokens representing a single variable declaration statement, and checks its legality and calculates its size on stack;
#######################################################################################################################################################
def parseVariableDeclaration(inputList):
	global typedefs, structuresAndUnionsDictionary, primitiveDatatypeLength
	PRINT ("="*30,"\nInside parseVariableDeclaration()\n","="*30,"\n" )
	PRINT ("inputList =",inputList )
	if not inputList:
		return False
	elif checkIfString(inputList):
		tokenizeLinesResult = tokenizeLines(inputList)
		if tokenizeLinesResult == False:
			PRINT ("ERROR in parseVariableDeclaration after calling tokenizeLines(inputList) for inputList (actually a string) =",inputList )
			return False
		else:
			tokenizeLinesOutput = tokenizeLinesResult[0]
			return parseVariableDeclaration(tokenizeLinesOutput)
	elif not isinstance(inputList,list):
		PRINT ("ERROR - Unknown input object to parseVariableDeclaration()", inputList," - exiting" )
		return False
		sys.exit()

	functionCheckResult = checkIfFunctionDefinition(inputList)
	if functionCheckResult[0]==False and ";" not in inputList:
		PRINT ("No semicolon in inputList" )
		errorMessage = "ERROR in parseVariableDeclaration() - every variable declaration must end with a semicolon - exiting"
		errorRoutine(errorMessage)
		return False
#				sys.exit()
	declarationEndIndex = len(inputList)
	if ';' in inputList:
		nextSemicolonIndex = inputList.index(";")
		declarationEndIndex = nextSemicolonIndex
	if functionCheckResult[0]==True:
		functionDeclarationEndIndex = functionCheckResult[1]
		declarationEndIndex = functionDeclarationEndIndex if functionDeclarationEndIndex < declarationEndIndex else declarationEndIndex
	
	if len(inputList) <3:
		PRINT ("ERROR in parseVariableDeclaration() - A variable declaration statement must have at least 3 terms" )
		return False
		sys.exit()
	elif inputList[declarationEndIndex] not in (";","}"):
		PRINT ("ERROR in parseVariableDeclaration() - A variable declaration statement must end with a semicolon" )
		return False
		sys.exit()
	elif not braceInterleavingLegal(inputList[:declarationEndIndex+1]):
		PRINT ("ERROR in parseVariableDeclaration() - A variable declaration statement contains braces that are not interleaved properly" )
		return False
		sys.exit()
		
	typeSpecifierEndIndex = findTypeSpecifierEndIndex(inputList)
	
	PRINT ("After calling findTypeSpecifierEndIndex() for inputList = ",STR(inputList),", the result typeSpecifierEndIndex =",typeSpecifierEndIndex )
	
	# Now that we know where the "base" type specifier ends, we perform a battery of checks to see if this is valid.
	
	if typeSpecifierEndIndex < 0:
		PRINT ("typeSpecifierEndIndex =",typeSpecifierEndIndex )
		errorMessage = "ERROR calling findTypeSpecifierEndIndex() for inputList = "+STR(inputList)
		errorRoutine(errorMessage)
		return False
	
	if 	typeSpecifierEndIndex <0 or typeSpecifierEndIndex > len(inputList)-3:	# The last two items must be at the minimum 2 items before the end of statement;
		PRINT ("ERROR in parseVariableDeclaration() - not enough tokens left after type specifier at typeSpecifierEndIndex=",typeSpecifierEndIndex,"for inputList =",inputList )
		PRINT ("inputList = ",inputList,"typedefs =",typedefs,"typedefs.keys() =",getDictKeyList(typedefs) )
		return False
		sys.exit()
	
	typeSpecifierList = inputList[:typeSpecifierEndIndex+1]

	baseTypeSpecifier = ['void','char','short','int','long','long long','float','double']
	typeSpecifierImplicit = ['signed','unsigned']     # TO-DO: need to add <struct-or-union-specifier> <enum-specifier> <typedef-name>
#	storageClassSpecifier = [ 'auto','register','static','extern','typedef']
#	typeQualifier = ['const','volatile']
	
	regularTypes = baseTypeSpecifier + typeSpecifierImplicit

	baseType = ""
	signedOrUnsigned = "signed"		# Default value

	# PORT: Another difference between PYTHON 2 and 3. For a dict.keys() yields a list for Python 2, but class of "dict_keys" for Python 3
	PRINT ("type(typedefs.keys()) = ",type(typedefs.keys()))
	PRINT ("type(enums.keys()) = ",type(enums.keys()))

	PRINT("typeSpecifierList =",typeSpecifierList)
	PRINT("getDictKeyList(structuresAndUnionsDictionary) =",getDictKeyList(structuresAndUnionsDictionary))

	# First check if there is any derived type
	derivedTypesIntypeSpecifierList 	= commonItems(typeSpecifierList, getDictKeyList(typedefs))
	structUnionTypesIntypeSpecifierList = commonItems(typeSpecifierList, getDictKeyList(structuresAndUnionsDictionary))
	enumTypesIntypeSpecifierList 		= commonItems(typeSpecifierList, getDictKeyList(enums))
	regularTypesIntypeSpecifierList 	= commonItems(typeSpecifierList, regularTypes)
	
	if derivedTypesIntypeSpecifierList:
		errorMessage = "ERROR in parseVariableDeclaration() for inputList = <%s> - we should never see any derived type (%s) in this routine, because all derived typed should have been re-converted into their original typedef form before "%(STR(inputList),STR(derivedTypesIntypeSpecifierList))
		errorRoutine(errorMessage)
		return False

	# Derived type - I coded this originally without realizing that this routine should never see any derived type. Still leaving it since no harm
	if len(derivedTypesIntypeSpecifierList)>1:
		errorMessage = "ERROR in parseVariableDeclaration(): We have multiple derived types (" + STR(derivedTypesIntypeSpecifierList) + ") for the same type declaration < " + STR(typeSpecifierList) + " >"
		errorRoutine(errorMessage)
		return False
	elif len(derivedTypesIntypeSpecifierList)==1:
		# For a derived type, we should not have any re-declaration
		if structUnionTypesIntypeSpecifierList or regularTypesIntypeSpecifierList:
			errorMessage = "ERROR in parseVariableDeclaration(): We have re-declaration (" + STR(structUnionTypesIntypeSpecifierList + regularTypesIntypeSpecifierList) + ") of already-derived type (" + STR(derivedTypesIntypeSpecifierList) + ") for the declaration < " + STR(typeSpecifierList) + " >"
			errorRoutine(errorMessage)
			return False
		else:
			baseType = derivedTypesIntypeSpecifierList[0]

	
	elif len(structUnionTypesIntypeSpecifierList)>1:	# pre-defined struct / union
		errorMessage = "ERROR in parseVariableDeclaration(): We have multiple struct/union types (" + STR(structUnionTypesIntypeSpecifierList) + ") for the same type declaration < " + STR(typeSpecifierList) + " >"
		errorRoutine(errorMessage)
		return False
	elif len(structUnionTypesIntypeSpecifierList)==1:
		# For a derived type, we should not have any re-declaration
		if regularTypesIntypeSpecifierList or enumTypesIntypeSpecifierList or derivedTypesIntypeSpecifierList:	# Checking for derivedTypesIntypeSpecifierList should be redundant
			errorMessage = "ERROR in parseVariableDeclaration(): We have re-declaration (" + STR(regularTypesIntypeSpecifierList) + STR(enumTypesIntypeSpecifierList) + STR(derivedTypesIntypeSpecifierList)+ ") of already-derived type (" + STR(structUnionTypesIntypeSpecifierList) + ") for the declaration < " + STR(typeSpecifierList) + " >"
			errorRoutine(errorMessage)
			return False
		else:
			baseType = structUnionTypesIntypeSpecifierList[0]

	elif len(enumTypesIntypeSpecifierList)>1:	# pre-defined enums
		errorMessage = "ERROR in parseVariableDeclaration(): We have multiple enum types (" + STR(enumTypesIntypeSpecifierList) + ") for the same type declaration < " + STR(typeSpecifierList) + " >"
		errorRoutine(errorMessage)
		return False
	elif len(enumTypesIntypeSpecifierList)==1:
		# For a derived type, we should not have any re-declaration
		if regularTypesIntypeSpecifierList or structUnionTypesIntypeSpecifierList or derivedTypesIntypeSpecifierList:	# Checking for derivedTypesIntypeSpecifierList should be redundant
			errorMessage = "ERROR in parseVariableDeclaration(): We have re-declaration (" + STR(regularTypesIntypeSpecifierList) + STR(structUnionTypesIntypeSpecifierList) + STR(derivedTypesIntypeSpecifierList)+ ") of already-derived type (" + STR(structUnionTypesIntypeSpecifierList) + ") for the declaration < " + STR(typeSpecifierList) + " >"
			errorRoutine(errorMessage)
			return False
		else:
#			baseType = enumTypesIntypeSpecifierList[0]
			baseType = "int"

	
	elif regularTypesIntypeSpecifierList:	# Regular declarations

		if noConflictingOccurrences(typeSpecifierList, ["float","double"]) == False:
			return False
		elif "float" in typeSpecifierList or "double" in typeSpecifierList:
			baseType = "float" if "float" in typeSpecifierList else "double"
			items2check = ["signed","unsigned","short","long","long long","char","int","void"]
			for item in items2check:
				if item in typeSpecifierList:
					errorMessage = "ERROR in parseVariableDeclaration(): for a base type of " + STR(baseType) + ", we cannot have conflicting " + STR(item) + " in type declaration < " + STR(typeSpecifierList) + " >"
					errorRoutine(errorMessage)
					return False
		if noConflictingOccurrences(typeSpecifierList, ["char","void"]) == False:
			return False
		elif "char" in typeSpecifierList or "void" in typeSpecifierList:
			baseType = "char" if "char" in typeSpecifierList else "void"
			items2check = ["short","int","long","long long"]
			for item in items2check:
				if item in typeSpecifierList:
					errorMessage = "ERROR in parseVariableDeclaration(): for a base type of " + STR(baseType) + ", we cannot have conflicting " + STR(item) + " in type declaration < " + STR(typeSpecifierList) + " >"
					errorRoutine(errorMessage)
					return False
		elif noConflictingOccurrences(typeSpecifierList, ["short","long","long long"]) == False:
			return False
		elif commonItems(typeSpecifierList,["short","long","long long"]):
			baseType = "short" if "short" in typeSpecifierList else "long" if "long" in typeSpecifierList else "long long"
		elif "int" in typeSpecifierList or "signed" in typeSpecifierList or "unsigned" in typeSpecifierList:
			baseType = "int"
		
		if baseType in ("char","short","int","long","long long"):
			if noConflictingOccurrences(typeSpecifierList, ["signed","unsigned"]) == False:
				return False
			elif "unsigned" in inputList[:typeSpecifierEndIndex+1]:
				signedOrUnsigned = "unsigned"

		# At this point, the baseType should be populated

		# It should never come here
	else:
		OUTPUT ("\n","==="*50)
		OUTPUT ("ERROR in parseVariableDeclaration(): The control should never have come here")
		OUTPUT ("typeSpecifierEndIndex =",typeSpecifierEndIndex,", typeSpecifierList =",typeSpecifierList)
		OUTPUT ("typedefs.keys() =", getDictKeyList(typedefs))
		OUTPUT ("derivedTypesIntypeSpecifierList =", derivedTypesIntypeSpecifierList)
		OUTPUT ("structuresAndUnionsDictionary.keys() =", getDictKeyList(structuresAndUnionsDictionary))
		OUTPUT ("structUnionTypesIntypeSpecifierList =",structUnionTypesIntypeSpecifierList)
		OUTPUT ("enums.keys() =", getDictKeyList(enums))
		OUTPUT ("enumTypesIntypeSpecifierList =",enumTypesIntypeSpecifierList)
		OUTPUT ("regularTypes =", regularTypes)
		OUTPUT ("regularTypesIntypeSpecifierList =",regularTypesIntypeSpecifierList)
		errorMessage = "ERROR in coding: Cannot resolve type declaration " + STR(typeSpecifierList)
		errorRoutine(errorMessage)
		return False

	PRINT ("Value of baseType =<" + STR(baseType) + "> in typeSpecifierList =<" + STR(typeSpecifierList) + ">")


	# Now, if there are any __attribute__ statements up to the typeSpecifierEndIndex, get their outputs.
	baseAttributes = {}		# This applies to ALL the variables declared by a single vairable declaration statement
	variableSpecificAttributes = {}		# This only applies to individual variables. This is additive to the baseAttributes
	
	k = 0
	while (k <= typeSpecifierEndIndex):
		if inputList[k] != ATTRIBUTE_STRING: 
			k += 1
		else:
			parseAttributeResult = parseAttribute(inputList[k:typeSpecifierEndIndex+1])
			if parseAttributeResult[0] != True:
				errorMessage = "ERROR in parseVariableDeclaration() after calling parseAttribute() for inputList[k(%d):typeSpecifierEndIndex(%d)+1] = <%s>]"%(k,typeSpecifierEndIndex,STR(inputList[k:typeSpecifierEndIndex+1]))
				errorRoutine(errorMessage)
				return False
			else:
				PRINT("parseAttributeResult[1] = ",parseAttributeResult[1])
				for (key, value) in parseAttributeResult[1].items():
					if (key == ALIGNED_STRING) and (ALIGNED_STRING in getDictKeyList(baseAttributes)):
						baseAttributes[key] = max(value, baseAttributes[key])
					else:
						baseAttributes[key] = value		# Yes, this will overwrite existing values, but we do not care
				d = parseAttributeResult[1]["distance"]
				k += 1+d+1

	PRINT ("baseAttributes =",baseAttributes)

	if (baseType == ""):
		errorMessage = "ERROR in parseVariableDeclaration(): Somehow illegal value of baseType =<" + STR(baseType) + "> in typeSpecifierList =<" + STR(typeSpecifierList) + ">"
		errorRoutine(errorMessage)
		return False

	i = typeSpecifierEndIndex+1
	
	declarationStatementEndReached = False
	
	# Now we have gotten the main variable type. Now, there might be multiple variable names defined in the same declaration statement.
	# Some of those variables might be pointers too.
	# We presume that every such declaration segment has a <leftBoundary>.
	# The rightBoundary will be a semicolon, comma, or a "=" when we are initializing
	
	returnListOf5tuples = []

	# For the first declaration
	leftBoundary = typeSpecifierEndIndex
	
	while i<len(inputList) and declarationStatementEndReached == False:
		# This code snippet below assumes that we have LEGAL C code. It will not work if you give it illegal C code where we have non-contiguous *
		# TO-DO: Handle that case
		
		PRINT ("\n\n","==="*50,"\nStarting new cycle of parsing from inputList[",i,"] = ", inputList[i],"\n","==="*50,"\n" )

		isBitField	= False
		isInitialized = False
		currentDeclarationSegmentStartIndex = i
		
		# There might be multiple levels of indirections and parenthesization. The first item not like that is the variable name.
		# TO-DO: Verify that this is indeed the correct assumption
		while True:
			if inputList[i] == "*" or inputList[i] == "(" : # TO-DO: const might appear here too
				i = i+1
			elif inputList[i] == ATTRIBUTE_STRING:
				parseAttributeResult = parseAttribute(inputList[i:])
				if parseAttributeResult[0] != True:
					errorMessage = "ERROR in parseVariableDeclaration() after calling parseAttribute() for inputList[i(%d):] = <%s>]"%(i,STR(inputList[i:]))
					errorRoutine(errorMessage)
					return False
				else:
					PRINT("parseAttributeResult[1] = ",parseAttributeResult[1])
					for (key, value) in parseAttributeResult[1].items():
						if key == ALIGNED_STRING and ALIGNED_STRING in getDictKeyList(variableSpecificAttributes):
							variableSpecificAttributes[key] = max(variableSpecificAttributes[key],value)
						else:
							variableSpecificAttributes[key] = value		
					d = parseAttributeResult[1]["distance"]
					i += 1+d+1
			else:
				break
		PRINT ("variableSpecificAttributes =",variableSpecificAttributes)
		
		if inputList[i] == "[" or inputList[i] == "[]" :
			PRINT("inputList =",inputList)
			errorMessage = "ERROR in parseVariableDeclaration(): Cannot have array on the base type itself: expected identifier or '(' before '[' token in inputList =<"+STR(inputList)+">"
			errorRoutine(errorMessage)
			return False
		
		# TO-DO: No variable name (bitwise alignment)
		variableNameIndex =  i
		variableName = inputList[variableNameIndex]
		
		if inputList[i] == ':':
			# Recall that the bitfield width need not be a straightaway number - it could be an arithmatic expression too
			if i+2 < len(inputList) and ('=' in inputList[i+2:] or ',' in inputList[i+2:] or ';' in inputList[i+2:]):
				PRINT("Found case of zero-width bitfield specifier (resets the bitfield boundary)");
				variableName = dummyZeroWidthBitfieldNamePrefix
			else:
				errorMessage = "ERROR in parseVariableDeclaration(): Illegal usage of <:> in bitfield specification for inputList =<"+STR(inputList)+">"
				errorRoutine(errorMessage)
				return False
		elif not re.match("^[_a-zA-Z]+[_0-9a-zA-Z]*",inputList[i]):
			errorMessage = "ERROR in parseVariableDeclaration(): <"+ STR(inputList[i])+"> is not a valid identifier name in inputList =<"+STR(inputList)+">"
			errorRoutine(errorMessage)
			return False
			
		variableDescription = variableName + " is"
		PRINT ("\n\n=======================================\nvariableNameIndex = ",variableNameIndex," variable name = ", variableName,"\n=======================================\n\n" )

		
		# The Q &D is to begin with the variable name, scan rightward until you hit a ")", then go back to the variable name and scan leftward until you hit a "(".
		# Then "step out" of the pair of braces, and repeat the process. For example, let's examine this really weird declaration:
		#
		#         void **(*(*weird)[6])(char, int);
		#
		# weird is a pointer to an array of 6 pointers to functions, each function accepting a char and an int as argument, and each returning a pointer to a pointer to void.
		#
		#
		# 		int (*Weirder(const char code)) (int, float) ;
		#
		# Weirder is a function that takes in a char as its argument, and returns a pointer to a function (basically a function pointer) 
		# that takes in (int, float) as its argument and returns an int.
		#

		# The way we implement this as follows. We need to "consume" the inputList[leftBoundary+1:]
		# There are two "counters" (I am not using the term pointer to avoid confusion). The "right" counter moves to the right, the "left" counter moves left.
		# Every time they move, they "consume" tokens. Once the "left" counter reaches leftBoundary and the "right" counter reaches the end, we are done;
		
#		PRINT ("Going to check the legal interleaving of braces in inputList[leftBoundary+1:] = inputList[",leftBoundary,"+1:] =",inputList[leftBoundary+1:], "has unmatched braces" )
		
		if not braceInterleavingLegal(inputList[leftBoundary+1:]):
			errorMessage = "ERROR in parseVariableDeclaration() - the inputList[leftBoundary+1:] =" + STR(inputList[leftBoundary+1:]) + "has unmatched braces" 
			errorRoutine(errorMessage)
			return False
			
		
		# Usually, we start scanning both to the left and right from the variableNameIndex. However, for zero-width bitfield, there is no variableNameIndex.
		leftCounterPrevious = leftCounter = variableNameIndex
		if variableName == dummyZeroWidthBitfieldNamePrefix:
			rightCounterPrevious = rightCounter = variableNameIndex -1
		else:
			rightCounterPrevious = rightCounter = variableNameIndex
		
		while (leftCounter>leftBoundary and rightCounter<len(inputList)-1):
			# First scan to the right
			rightCounter = rightCounter + 1
			if inputList[rightCounter]==")":
				if matchingBraceDistanceReverse(inputList[:rightCounter+1]) < 1:
					errorMessage = "ERROR in parseVariableDeclaration(): Cannot find matching brace in reverse in " +STR(matchingBraceDistanceReverse(inputList[:rightCounter+1]))+ " - exiting!!" 
					errorRoutine(errorMessage)
					return False
				leftCounter = rightCounter - matchingBraceDistanceReverse(inputList[:rightCounter+1])
				if leftCounter >= leftCounterPrevious:	# Should never happen
					PRINT ("ERROR - leftCounter =", leftCounter, "leftCounterPrevious =",leftCounterPrevious )
					sys.exit()
				if leftCounter < leftCounterPrevious:	# Should always happen
					# Verify that all intermediate tokens are '*' only
					k = leftCounter + 1
					while k < leftCounterPrevious:
						if inputList[k] == "*":
							variableDescription = variableDescription + " pointer to "
						else:
							errorMessage = "ERROR in parseVariableDeclaration() - unexpected token inputList["+STR(k)+"] =" + STR(inputList[k])
							errorRoutine(errorMessage)
							return False
						k = k + 1
				leftCounterPrevious = leftCounter
				rightCounterPrevious = rightCounter
			elif inputList[rightCounter]=="[" or inputList[rightCounter]=="[]":
				PRINT ("\n\n\nHit an array - Currently, variableDescription =<%s>\n\n\n"%variableDescription)
				# We need to handle the case that a function cannot return an array.
				str2search = "and returns a "
				if len(variableDescription)>len(str2search) and ("function" in variableDescription) and (variableDescription[-len(str2search):]==str2search):
					errorMessage = "ERROR in parseVariableDeclaration() - the inputList =" + STR(inputList) + " has a function returning an array" 
					errorRoutine(errorMessage)
					return False
				 
			
				# We have a problem of when a multi-dimensional array is declared with parenthesis in between the array dimensions, like int (a[2])[3]; instead of just int a[2][3];
				# In that case, instead of producing "array of size 2 X 3", the code might produce "array of size 2 array of size 3".
				# To prevent this kind of things, we first check if the current variableDescription is already ending with array declaration (like "array of size 2".
				# If yes, instead of adding yet another "array of size 3", we just add " X 3".
				if re.search(r" array of size\s+\d+(\s+X\s+\d+)*\s*$",variableDescription):
					PRINT ("variableDescription = <%s> currently ends with an \"array of size N\" kind of statement"%variableDescription )
					variableDescription = variableDescription + " X "
				else:
					PRINT ("variableDescription = <%s> does not end with an \"array of size N\" kind of statement"%variableDescription )
					variableDescription = variableDescription + " array of size "
				k = rightCounter
				dimensionCount = 0
				# Our current tokenizer combines "()" or "[]" into a single token if there is no space in between (TO-DO)
				while (inputList[k]=="[" or inputList[k]=="[]"):
					dimensionCount = dimensionCount + 1
					if inputList[k]=="[]": # Array size NOT specified
						matchingBraceIndex = k
						PRINT ("Array size NOT specified for ARRAY variable",variableName )
						if dimensionCount > 1:
							PRINT ("ERROR in parseVariableDeclaration() - array size must be specified for array level",dimensionCount )
							return False
							sys.exit()
						else:
							variableDescription = variableDescription + "TBD"
					else:
						if matchingBraceDistance(inputList[k:]) < 1:
							PRINT ("Cannot find matching brace distance for ",inputList[k:] )
							return False
							sys.exit()
						matchingBraceIndex = k + matchingBraceDistance(inputList[k:])
#						PRINT ("matchingBraceIndex =",matchingBraceIndex )
						if dimensionCount > 1:
							variableDescription = variableDescription + " X "
						# This code block below will never be hit in our current Tokenizer (which considers "[]" a single token), still kept for future-proofing
						if matchingBraceIndex == k+1: # Array size NOT specified
							PRINT ("Array size NOT specified for array variable <",variableName,">" )
							if dimensionCount > 1:
								PRINT ("ERROR in parseVariableDeclaration() - array size must be specified for array level",dimensionCount )
								return False
								sys.exit()
							else:
								variableDescription = variableDescription + "TBD"
						else:
							parseArithmeticExpressionOutput = parseArithmeticExpression(inputList[k+1:matchingBraceIndex])
							if parseArithmeticExpressionOutput == False:
								PRINT ("ERROR after calling parseArithmeticExpression(inputList[k+1:matchingBraceIndex]) for inputList[",k,"+1:",matchingBraceIndex,"] = ",inputList[k+1:matchingBraceIndex] )
								return False
								sys.exit()
							else:
								evaluateArithmeticExpressionOutput = evaluateArithmeticExpression(parseArithmeticExpressionOutput)
								if evaluateArithmeticExpressionOutput[0] != True:
									PRINT ("ERROR while calculating array dimensions, after calling evaluateArithmeticExpression(parseArithmeticExpressionOutput) for parseArithmeticExpressionOutput =",parseArithmeticExpressionOutput )
									errorMessage = "ERROR in parseVariableDeclaration() - array dimension <%s> not a proper arithmetic expression"%(STR(inputList[k+1:matchingBraceIndex]))
									errorRoutine(errorMessage)
									return False
								elif evaluateArithmeticExpressionOutput[1] <1:
									errorMessage = "ERROR in parseVariableDeclaration() - array dimension <%s> evaluates to %d, which is not allowed"%(list2plaintext(inputList[k+1:matchingBraceIndex]),evaluateArithmeticExpressionOutput[1])
									errorRoutine(errorMessage)
									return False
								
								variableDescription = variableDescription + str(evaluateArithmeticExpressionOutput[1])
					k = matchingBraceIndex + 1
				rightCounter = matchingBraceIndex
				rightCounterPrevious = rightCounter
			# Our current tokenizer combines "()" or "[]" into a single token (TO-DO)
			elif inputList[rightCounter]=="(" or inputList[rightCounter]=="()":
#				PRINT ("pointer to " )
				rightCounterPrevious = rightCounter
				if inputList[rightCounter]=="()":
					variableDescription = variableDescription + " of type function that accepts no Argument and returns a "
				else:
					if matchingBraceDistance(inputList[rightCounter:]) < 1:
						PRINT ("No match for ",inputList[rightCounter:]," ... exiting" )
						return False
						sys.exit()
					rightCounter = rightCounter + matchingBraceDistance(inputList[rightCounter:])
					argList = parseArgumentList(inputList[rightCounterPrevious:rightCounter+1])
					if argList == False:
						PRINT ("Error while parsing the argument list in ",inputList[rightCounterPrevious:rightCounter+1]," - exiting!" )
						return False
						sys.exit()
					variableDescription = variableDescription + " of type function that accepts Argument list "  + str(argList) + " and returns a "
				rightCounterPrevious = rightCounter
		
			########################################################################################
			# Handle bitfields		
			#########################################################################################
			elif inputList[rightCounter]==":":

				# TO-DO: Need to handle the case of no-variable-name bitfield (only for aligning)

			
				rightCounter = rightCounter+1		# Consume the ":"
				PRINT ("Bitfield variable!!!")
				
				PRINT ("Current variableDescription = <",variableDescription,">")
				
				if baseType not in ("char","short","int","long","long long"):
					errorMessage = "ERROR: bit field declataion not allowed for baseType = <" + STR(baseType) +">)"
					errorRoutine(errorMessage)
					return False
				elif "*" in inputList[currentDeclarationSegmentStartIndex:variableNameIndex]:
					errorMessage = "ERROR: Pointer not allowed for bit field declataion for "+STR(variableName)
					errorRoutine(errorMessage)
					return False
				elif "array of size" in variableDescription:
					errorMessage = "ERROR: Arrays not allowed for bit field declataion for "+STR(variableName)
					errorRoutine(errorMessage)
					return False
				
				bitFieldWidthExpressionStartIndex = rightCounter
				
				# We are assuming that by now all the preprocessing (macro stuff) etc. has happened. Hence, we are assuming that there are no commas within the bitfield width.
				# TO-DO: Verify that there cannot really be any comma.
				nextCommaIndex = 10000000000000		# Arbitrarily large value
				nextEqualToIndex = 10000000000000	# Arbitrarily large value
				nextSemicolonIndex = rightCounter + inputList[rightCounter:].index(';')
				if ',' in inputList[rightCounter:nextSemicolonIndex]:
					nextCommaIndex = rightCounter + inputList[rightCounter:nextSemicolonIndex].index(',')
				if '=' in inputList[rightCounter:nextSemicolonIndex]:
					nextEqualToIndex = rightCounter + inputList[rightCounter:nextSemicolonIndex].index('=')
				bitFieldWidthExpressionEndIndexInclusive = min(nextSemicolonIndex,nextCommaIndex,nextEqualToIndex)-1
				bitFieldWidthExpression = inputList[bitFieldWidthExpressionStartIndex:bitFieldWidthExpressionEndIndexInclusive+1]
				PRINT ("The bitfield width expression is from start index ",bitFieldWidthExpressionStartIndex, "to end index ",bitFieldWidthExpressionEndIndexInclusive,"(inclusive) = ",bitFieldWidthExpression)

				parseArithmeticExpressionOutput = parseArithmeticExpression(bitFieldWidthExpression)
				if parseArithmeticExpressionOutput == False:
					errorMessage = "ERROR after calling parseArithmeticExpression(bitFieldWidthExpression = <" + STR(bitFieldWidthExpression) +">)"
					errorRoutine(errorMessage)
					return False
					sys.exit()
				else:
					evaluateArithmeticExpressionOutput = evaluateArithmeticExpression(parseArithmeticExpressionOutput)
					if evaluateArithmeticExpressionOutput[0] != True:
						errorMessage = "ERROR in bitfield width calculation after calling evaluateArithmeticExpression(parseArithmeticExpressionOutput) for parseArithmeticExpressionOutput ="+ STR(parseArithmeticExpressionOutput)
						errorRoutine(errorMessage)
						return False
					else:
						bitFieldWidth = evaluateArithmeticExpressionOutput[1]
						if bitFieldWidth > primitiveDatatypeLength[baseType]*BITS_IN_BYTE:
							errorMessage = "ERROR: Bitfield width of " + STR(bitFieldWidth) + "cannot be larger than the size (" + STR(primitiveDatatypeLength[baseType]) + ") of the base datatype (" +STR(baseType)+")"
							errorRoutine(errorMessage)
							return False
						elif bitFieldWidth < 0:
							errorMessage = "ERROR: Bitfield width of " + STR(bitFieldWidth) + "cannot be negative for bit variable " + variableName
							errorRoutine(errorMessage)
							return False
						elif bitFieldWidth == 0 and variableName != dummyZeroWidthBitfieldNamePrefix:
							errorMessage = "ERROR: Bitfield width of " + STR(bitFieldWidth) + "cannot be 0 for bit variable " + variableName
							errorRoutine(errorMessage)
							return False
						else:
							isBitField = True
							PRINT (variableName,"is a bitfield,",bitFieldWidth,"bits wide")
							rightCounterPrevious = rightCounter
							rightCounter = bitFieldWidthExpressionEndIndexInclusive

			######################################################################################
			# Handle the __attribute__ statements at the end of individual variable declaration
			######################################################################################
			elif inputList[rightCounter]== ATTRIBUTE_STRING:
				while True:
					if inputList[rightCounter] == ATTRIBUTE_STRING:
						parseAttributeResult = parseAttribute(inputList[rightCounter:])
						if parseAttributeResult[0] != True:
							errorMessage = "ERROR in parseVariableDeclaration() after calling parseAttribute() for inputList[rightCounter(%d):] = <%s>]"%(rightCounter,STR(inputList[rightCounter:]))
							errorRoutine(errorMessage)
							return False
						else:
							PRINT("parseAttributeResult[1] = ",parseAttributeResult[1])
							for (key, value) in parseAttributeResult[1].items():
								if key == ALIGNED_STRING and ALIGNED_STRING in getDictKeyList(variableSpecificAttributes):
									variableSpecificAttributes[key] = max(variableSpecificAttributes[key], value)
								else:
									variableSpecificAttributes[key] = value		# Yes, this will overwrite existing values, but we do not care
							d = parseAttributeResult[1]["distance"]
							rightCounter += 1+d	# We do not advance the counter to the next token - that will automatically be done the first thing within the while loop
							PRINT("After processing the __attribute__, inputList[rightCounter(",rightCounter,")] =",inputList[rightCounter])
					else:
						break
				PRINT ("variableSpecificAttributes =",variableSpecificAttributes)

			###########################################################################
			# Handle End of individual variable declaration, including initialization
			###########################################################################
#			elif inputList[rightCounter]=="{":
#				MUST_PRINT("variableDescription =",variableDescription)
#				MUST_PRINT("variableName = inputList[",variableNameIndex,"] =",variableName)
#				MUST_PRINT("rest of inputList =",inputList[rightCounter:])
			elif ((variableDescription.startswith(variableName+" is of type function") and inputList[rightCounter]=="{" and rightCounter<len(inputList)-1 and '}' in inputList[rightCounter+1:]) 
			     or inputList[rightCounter]==";" or inputList[rightCounter]=="," or inputList[rightCounter]=="="):
			    
				if leftBoundary < leftCounter:	# Should always happen
					# Verify that all intermediate tokens are '*' only
					# TO-DO: Can const be here?
					k = leftCounter - 1
					while k > leftBoundary:
						if inputList[k] == "*":
							variableDescription = variableDescription + " pointer to "
						else:
							PRINT ("ERROR in parseVariableDeclaration() during end-of-declaration and initialization - unexpected token inputList[",k,"] =",inputList[k] )
							return False
							sys.exit
						k = k - 1

				if inputList[rightCounter] == '=':	# Initialization
					if "typedef" in inputList[:typeSpecifierEndIndex+1]:
						errorMessage = "ERROR in parseVariableDeclaration("+STR(inputList)+") - initialization not allowed for TYPEDEF variable "+STR(variableName)+" since derived types by themselves hold no storage"
						errorRoutine(errorMessage)
						return False
					isInitialized = True
					initializationStartIndex = rightCounter
					rightCounter = rightCounter+1		# Consume the "="
					nextCommaIndex = -10000
					nextSemicolonIndex = rightCounter + inputList[rightCounter:].index(';')
					if ',' in inputList[rightCounter:]:
						# Remember that a comma can be also part of an array initialization
						k = rightCounter
#						PRINT ("Checking initialization value - inspecting", inputList[k:] )
						while k < len(inputList):
							if inputList[k] == "(" or inputList[k] == "{" or inputList[k] == "[":
								d = matchingBraceDistance(inputList[k:])
								if d < 1:
									PRINT ("Cannot find matching distance for",inputList[k:]," - exiting" )
									return False
									sys.exit()
#								PRINT ("Found brace",inputList[k]," at k =",k,"corresponding match is at distance",d )
								k = k + d + 1
#								PRINT ("k value incremented to ",k )
							elif inputList[k] == ",":
								nextCommaIndex = k
								break
							else:
								k = k + 1
					
					if nextCommaIndex >= 0 and nextCommaIndex < nextSemicolonIndex:
						initializationEndIndex = nextCommaIndex - 1
					else:
						initializationEndIndex = nextSemicolonIndex-1;
					initializationValue = inputList[rightCounter:initializationEndIndex+1]
#					PRINT ("variableName ",variableName,"is initialized to the value",initializationValue )
					rightCounter = initializationEndIndex+1
					if initializationEndIndex == nextSemicolonIndex-1:
						declarationStatementEndReached = True

				# We do want to keep the function declarations, but we want to ignore actual function implementations. So when we realize that found an implementation,
				# we just note down its implementation as its initialization value.
				elif (variableDescription.startswith(variableName+" is of type function") and inputList[rightCounter]=="{" and rightCounter<len(inputList)-1 and '}' in inputList[rightCounter+1:]):
					initializationStartIndex = rightCounter
					currentDeclarationSegmentEndIndexInclusive = rightCounter + matchingBraceDistance(inputList[rightCounter:])
					rightCounter = currentDeclarationSegmentEndIndexInclusive
					isInitialized = True
					initializationValue = inputList[initializationStartIndex:currentDeclarationSegmentEndIndexInclusive+1]
				else:
					initializationValue = ""
					
				# Reset the leftBoundary for the next segment of variable declaration, if any
				leftBoundary = rightCounter
				
				currentDeclarationSegmentEndIndexInclusive = rightCounter
				
#		variableDescription = variableDescription + " of type " + ("unsigned " if signedOrUnsigned == "unsigned" else "")+ inputList[typeSpecifierEndIndex] 
		variableDescription = variableDescription + " of type " + ("unsigned " if signedOrUnsigned == "unsigned" else "")+ baseType 
		if initializationValue != "":
			variableDescription = variableDescription + ", which is initialized to the value " + str(initializationValue)
		
		PRINT ("For variable <", variableName, ">, variableDescription = ",variableDescription )
#		sys.exit()

		# Calculate the size of the variable
		# The strategy is: We try to find out if the variable is an array or not. If it is an array, its size
		
		isArray = False		# Default value
		
		maxSize = len(variableDescription) + 1	#just an arbitrarily large index that is larger than the possible index value
		tempStr = variableDescription.strip().split(variableName+" is ")[1].strip()
		PRINT ("tempStr =", tempStr )
		
		size = -1  #just giving a wrong value
		multiplier = 1
		arrayDimensions = []	# If this is an array, it will give the array dimensions. Otherwise, it will be blank
		PRINT ("\n\nGoing to determnine the size of tempStr=<%s>\n\n"%(tempStr) )
		# If tempStr starts with the word "pointer to", then we know right away its size
		arrayOfSizeStr = "array of size "
		if (len(tempStr)>=len(arrayOfSizeStr)) and (tempStr[0:len(arrayOfSizeStr)] == arrayOfSizeStr):
			PRINT ("Detected ARRAY ! ! !" )
			isArray = True
			restOfString = tempStr[len(arrayOfSizeStr):].split(" ")
			PRINT ("restOfString =",restOfString )
			totalNumberOfArrayElements = int(restOfString[0])
			arrayDimensions.append(totalNumberOfArrayElements)
			k = 1
			
			# Thanks to typedefs, we could end up with multiple "array of size 2 array of size 3" statement instead of a simple "array of size 2 X 3" statement
			while (restOfString[k] == "X") or (len(restOfString)>=k+4 and restOfString[k:k+3]==["array","of","size"]):
				PRINT ("Multi-dimensional array detected!" )
				if restOfString[k] == "X":
#					PRINT ("k = ",k,"restOfString[k] =",restOfString[k], "restOfString[k+1] =",restOfString[k+1] )
					newArrayDimension = int(restOfString[k+1])
					totalNumberOfArrayElements = totalNumberOfArrayElements * newArrayDimension
					PRINT ("Adding new dimension of",newArrayDimension,"; now totalNumberOfArrayElements =",totalNumberOfArrayElements )
					arrayDimensions.append(newArrayDimension)
					k = k + 2
				elif len(restOfString)>=k+4 and restOfString[k:k+3]==["array","of","size"]:
					newArrayDimension = int(restOfString[k+3])
					totalNumberOfArrayElements = totalNumberOfArrayElements * newArrayDimension
					PRINT ("Adding new dimension of",newArrayDimension,"; now totalNumberOfArrayElements =",totalNumberOfArrayElements )
					arrayDimensions.append(newArrayDimension)
					k = k + 4
				else:
					PRINT ("ERROR in parseVariableDeclaration(): We should have never been here" )
					sys.exit()
			multiplier = totalNumberOfArrayElements
			PRINT ("multiplier =",multiplier )
			PRINT ("BEFORE RE substituion, tempStr = <%s>"%(tempStr) )
			tempStr = re.sub(r"^(array of size\s+\d+(\s+X\s+\d+)*\s+)+","",tempStr)
			PRINT ("AFTER RE substituion, tempStr = <%s>"%(tempStr) )
		if tempStr[0:7] == "pointer":
			datatype = "pointer"
			size = 4
		elif tempStr[0:7] == "of type":
			datatype = tempStr[8:]
			PRINT ("Checking for datatype = <%s>"%(datatype) )
			if datatype.startswith("unsigned"):
				datatype = datatype[9:]
			if datatype.startswith("function"):
				size = 0	# A function pointer has a size. A function does not need any storage. Pure C does not allow structs to have functions in them.
			elif datatype in getDictKeyList(primitiveDatatypeLength):
				size = primitiveDatatypeLength[datatype]
			elif datatype in getDictKeyList(typedefs):
				# It typedefs into a structure/union
				if isinstance(typedefs[datatype],list) and len(typedefs[datatype])==2 and (typedefs[datatype][0] == "enum" or typedefs[datatype][0] == "struct" or typedefs[datatype][0] == "union"):
					structOrUnionName = typedefs[datatype][1]
					PRINT ("Checking for size of datatype", datatype,"which is actually a ",typedefs[datatype][0],structOrUnionName )
					if structuresAndUnionsDictionary[structOrUnionName] and ("size" in structuresAndUnionsDictionary[structOrUnionName]):
						size = int(structuresAndUnionsDictionary[structOrUnionName]["size"])
					else:
						PRINT ("ERROR in parseVariableDeclaration() - unknown size of struc/union datatype <",structOrUnionName,"> - exiting" )
						PRINT ("typedefs = ",typedefs )
						PRINT ("structuresAndUnionsDictionary =",structuresAndUnionsDictionary )
						return False
						sys.exit()
				# It typedefs into some other regular variable declaration
				else: 
					item = typedefs[datatype]
					PRINT ("The typedef", datatype,"resolves into",item )
					if len(item) != 5:
						PRINT ("ERROR in parseVariableDeclaration() - unknown tuple - exiting" )
						return False
						sys.exit()
					else:
						size = typedefs[datatype][1]
			elif datatype in getDictKeyList(enums):
				# In C, enum sizes are not specified of at least an INT
				size=primitiveDatatypeLength["int"]
				PRINT ("The size of Enum <",datatype,"> is assumed to be same as an Integer,",size )
				
			elif datatype in getDictKeyList(structuresAndUnionsDictionary):
				PRINT ("Checking for size of datatype", datatype )
				if "size" in structuresAndUnionsDictionary[datatype]:
					size = int(structuresAndUnionsDictionary[datatype]["size"])
				else:
					PRINT ("ERROR in parseVariableDeclaration() - unknown size of struc/union datatype <",datatype,"> - exiting" )
					PRINT ("typedefs = ",typedefs )
					PRINT ("structuresAndUnionsDictionary =",structuresAndUnionsDictionary )
					return False
					sys.exit()
			else:
				PRINT ("ERROR in parseVariableDeclaration() - unknown datatype <",datatype,"> - exiting" )
				PRINT ("typedefs = ",typedefs )
				PRINT ("structuresAndUnionsDictionary =",structuresAndUnionsDictionary )
				return False
				sys.exit()
		else:
			PRINT ("ERROR in parseVariableDeclaration() - how did we end up here? tempStr = <",tempStr,"> - exiting" )
			return False
			sys.exit()
			
		arrayElementSize = size		# Size of a single array element
#		PRINT ("size =",size,"multiplier =",multiplier )
		size = size * multiplier 	# Size of the whole
#		PRINT ("After size = size * multiplier, now size =",size )

		if isArray != True and isArray != False:	# Just doubly making sure
			PRINT ("ERROR - illegal value for isArray = <",isArray,"> - exiting!" )
			sys.exit()
		
		# Observe that we have added one extra element (typeSpecifierEndIndex) to this list. We store this because this is one item that can NEVER be recovered later.
		# The reason is, suppose we are having recursive typedef statements. 
		#
		# 		typedef int INT2[2];
		#		typedef INT2 INT3[3];
		#
		# Now, when we are doing this compilation the line "typedef INT2 INT3[3];" for the first time, INT3 is not yet part of the typedefs dictionary (though INT2 is).
		# So the typeSpecifierEndIndex will stop at INT2. However, once this statement is compiled, if we for some reason re-compile this, now INT3 is also part of the typedefs,
		# so typeSpecifierEndIndex will now stop at INT3, which is wrong. So, in order to preserve the compile-time-environment for the first-time-compilation, we need to
		# store this item separately.
		
		# Merge the baseAttributes and variableSpecificAttributes. Overwrites will happen except in case of Aligned, where the max value will prevail
		attributes = {}
		for key,value in baseAttributes.items():
			attributes[key] = value
		for key,value in variableSpecificAttributes.items():
#			if key == ALIGNED_STRING and ALIGNED_STRING in getDictKeyList(variableSpecificAttributes):	# Possible bug?
			if key == ALIGNED_STRING and ALIGNED_STRING in getDictKeyList(attributes):
				attributes[key] = max(value,attributes[key])
			else:
				attributes[key] = value
			
		variableDescriptionExtended = {}
		variableDescriptionExtended["isArray"]=isArray
		variableDescriptionExtended["isBitField"]=isBitField
		if isBitField: 
			variableDescriptionExtended["bitFieldWidth"]=bitFieldWidth
		variableDescriptionExtended["description"]=variableDescription
		variableDescriptionExtended["arrayDimensions"]=arrayDimensions
		variableDescriptionExtended["datatype"]=datatype		# For  int * pInt; baseType is int, but datatype is pointer. That's the difference between baseType and datatype
																# for a declaration like "struct A a; ", the datatype is simply "A", not the list ['struct', 'A']
		variableDescriptionExtended["baseType"]=baseType		# It is the void/char/short/int/long/long long/float/double used in the variable declaration statement.
																# for a declaration like "struct A a; ", the baseType is simply "A", not the list ['struct', 'A']
		variableDescriptionExtended["signedOrUnsigned"]=signedOrUnsigned
		variableDescriptionExtended["arrayElementSize"]=arrayElementSize
		variableDescriptionExtended["typeSpecifierEndIndex"]=typeSpecifierEndIndex
		variableDescriptionExtended["variableNameIndex"]=variableNameIndex
		variableDescriptionExtended["currentDeclarationSegmentStartIndex"]=currentDeclarationSegmentStartIndex 
		variableDescriptionExtended["currentDeclarationSegmentEndIndexInclusive"]=currentDeclarationSegmentEndIndexInclusive
		variableDescriptionExtended["isInitialized"]=isInitialized
		if isInitialized:
			variableDescriptionExtended["initializationStartIndex"]=initializationStartIndex
		if attributes:
			variableDescriptionExtended["attributes"]=attributes
		
		# "type" : "struct/union", 
		# "size":size, 
		# "components":[[variable1 name, variable size, variable declaration statement, variable name Index within the declaration tokenList, variable description],...]}
		PRINT ("Now going to append to returnList, whose current content is" )
		for item in returnListOf5tuples:
			PRINT (item )
		returnList = []
		returnList.append(variableName)
		returnList.append(size)							# Variable size - for array, total size of ALL array elements combined
		returnList.append(inputList)
		returnList.append(variableNameIndex)	# This may look redundant now because we already have the variable name, but it will come handy later locating the variable position for coloring
		returnList.append(variableDescriptionExtended)
		
		returnListOf5tuples.append(returnList)
		
		i = rightCounter + 1

	if "typedef" in inputList[:typeSpecifierEndIndex+1]:	# The "typedef" can be anywhere within the base specifier
		for item in returnListOf5tuples:
			PRINT ("\n\n=============$$$$$$============\nAdding NEW typedef!!!\n=============$$$$$$============\n\n" )
			PRINT ("Adding typedefs[",item[0],"] =",item )
			typedefs[item[0]]=item
			
	PRINT ("returnListOf5tuples = ",returnListOf5tuples )
	return returnListOf5tuples


#str1 = "void **(*(*weird)[][7][8])(   ) = 3;"
#str1 = "int **x={a,b}, y[][1+7*8];"
#inputList=tokenizeLines(str1)
#parseVariableDeclaration(inputList)
#sys.exit()


############################################################################
#  What this routine does is the following:
#
#  It takes as input an array of lines.
#
#  If the first line contains an #if, #ifdef or #ifndev (basically any preprocessor if statement),
#  then it will return an array of [lineNumber, token] where the tokens are the conditional ones.
# 
#  For example, suppose the program structure (with line numebrs is this)
# 
#  Line # 0: #if (some condition)
#  ...
#  Line # 4: #ifdef something
#  ...
#  Line # 7: #endif
#  Line # 8: #elif (some other condition)
#  ...
#  Line # 9: #elif (some other condition)
#  ...
#  Line # 15: #endif
#                                                                          
# This routine will return [ [0,"#if"], [8,"#elif"], [9,"#elif"], [15, "#endif"]
#
############################################################################
def checkPreprocessingDirectivesInterleaving(inputLines):

	if not inputLines:
		return []
	
	# Check that inputLines is a list of Lines (strings ending with a newline). If it is a single string, make it a list
	if  isinstance(inputLines,list):
#		PRINT ("inputLines is indeed a list" )
		itemCount = 0
		while itemCount < len(inputLines):
			if not checkIfString(inputLines[itemCount]):
				PRINT ("Exiting - inputLines is not a list of proper strings - ", inputLines )
				return False
				sys.exit()
			elif not inputLines[itemCount] or inputLines[itemCount][-1] != '\n':
				inputLines[itemCount] = inputLines[itemCount] + '\n'
			itemCount = itemCount + 1
#		PRINT ("inputLines is indeed a list of proper strings - ", inputLines )
	else:
#		PRINT ("inputLines is NOT a list" )
		if checkIfString(inputLines):
#			PRINT (("Checking if inputLines=<%s> has a newline at the end"%(inputLines)) )
			if inputLines[-1] != '\n':
#				PRINT ("Appending newline to the end of inputLines" )
				inputLines = inputLines + '\n'
#			PRINT ("Converting the inputLines <",inputLines,">, which is a basic string but not a list, into a list" )
			inputLines = [inputLines]
#			PRINT ("Now the listified inputLines = ",inputLines )
		else:
			PRINT ("Exiting - Unknown object type - inputLines = <",inputLines,">" )
			return False
			sys.exit()

	#preprocessingDirectives = ('#include', '#if', '#ifdef', '#ifndef', '#else', '#elif', '#endif', '#define', '#undef', '#line', '#error', '#pragma')

	# This essentially only keeps those lines starting with a preprocessingDirectives. We note the preprocessingDirective and its line number, and its nesting level
	onlyPreprocessingDirectives = []
	tempStack = []
	lineNumber = 0
	nestingLevel = -1
	while lineNumber < len(inputLines):
		currLine = inputLines[lineNumber]
		tokenizeLinesResult = tokenizeLines(currLine)
		if tokenizeLinesResult == False:
			PRINT ("ERROR in checkPreprocessingDirectives after calling tokenizeLines(currLine) for currLine =",currLine )
			return False
		else:
			currLineTokenList = tokenizeLinesResult[0]
			if currLineTokenList and currLineTokenList[0] in preprocessingDirectives:
				if currLineTokenList[0] in ('#if', '#ifdef', '#ifndef'):
					nestingLevel += 1
					onlyPreprocessingDirectives.append([lineNumber, currLineTokenList[0], nestingLevel])
					tempStack.append(currLineTokenList[0])
				elif currLineTokenList[0] in ('#elif','#else'):
					onlyPreprocessingDirectives.append([lineNumber, currLineTokenList[0], nestingLevel])
					tempStack.append(currLineTokenList[0])
				elif currLineTokenList[0] == '#endif':
					onlyPreprocessingDirectives.append([lineNumber, currLineTokenList[0],nestingLevel])
					if tempStack[-1] ==  '#else':
						del tempStack[-1]
					while True:
						if tempStack[-1] ==  '#else':
							errorMessage = "The interleaving of if-then-else at the preprocessor level is not correct - multiple #else"
							errorRoutine(errorMessage)
							return False
						elif tempStack[-1] ==  '#elif':
							del tempStack[-1]
						else:
							break
					if tempStack[-1] in ('#if', '#ifdef', '#ifndef'):
						del tempStack[-1]
					else:
						errorMessage = "The interleaving of if-then-else at the preprocessor level is not correct"
						errorRoutine(errorMessage)
						return False
					nestingLevel -= 1
				else:
					PRINT("Ignoring preprocessingDirectives currLineTokenList[0] =",currLineTokenList[0])
			else:
				PRINT("Ignoring non-preprocessingDirective currLine =",currLine)
		lineNumber += 1
	
	if tempStack:	# Should be empty
		errorMessage = "The interleaving of if-then-else at the preprocessor level is not correct"
		errorRoutine(errorMessage)
		return False
		
	PRINT("onlyPreprocessingDirectives =",onlyPreprocessingDirectives)
	
	# Now see if this is a legal interleaving of the outermost (nesting level 0) preprocessingDirectives
	returnValue = []
	i = 0
	while i<len(onlyPreprocessingDirectives):
		if onlyPreprocessingDirectives[i][2] == 0:	# We are only interested in nesting level of 0
			returnValue.append([onlyPreprocessingDirectives[i][0],onlyPreprocessingDirectives[i][1]])
		i += 1
		
	# Sanity check - it must start with a mandatory single if, followed by optional elifs, followed by a single optional else, followed by a signle mandatory endif
	if len(returnValue) <2:
		errorMessage = "An if-then-else must have at least two rows (the beginning if and the ending endif)"
		errorRoutine(errorMessage)
		return False
	elif returnValue[0][1] not in ('#if', '#ifdef', '#ifndef'):
		errorMessage = "The first term must be '#if', '#ifdef', or '#ifndef'"
		errorRoutine(errorMessage)
		return False
	elif returnValue[-1][1] not in ('#endif'):
		errorMessage = "The last term must be '#endif'"
		errorRoutine(errorMessage)
		return False
	elif len(returnValue)>2:
		ifCount = 0
		elifCount = 0
		elseCount = 0
		endifCount = 0
		for row in returnValue:
			if row[1] in ('#if', '#ifdef', '#ifndef'):
				ifCount += 1
			elif row[1] in ('#elif'):
				elifCount += 1
			elif row[1] in ('#else'):
				elseCount += 1
			elif row[1] in ('#endif'):
				endifCount += 1
		if ifCount + elifCount + elseCount + endifCount != len(returnValue):
			errorMessage = "ERROR in checkPreprocessingDirectivesInterleaving() - ifCount(%d) + elifCount(%d) + elseCount(%d) + endifCount(%d) != len(returnValue)(%d)"%(ifCount, elifCount, elseCount, endifCount, len(returnValue))
			errorRoutine(errorMessage)
			return False
		elif ifCount > 1:
			errorMessage = "ERROR in checkPreprocessingDirectivesInterleaving() - multiple #if/#ifdef/#ifndef statements"
			errorRoutine(errorMessage)
			return False
		elif elseCount > 1:
			errorMessage = "ERROR in checkPreprocessingDirectivesInterleaving() - multiple #else statements"
			errorRoutine(errorMessage)
			return False
		elif endifCount > 1:
			errorMessage = "ERROR in checkPreprocessingDirectivesInterleaving() - multiple #endif statement"
			errorRoutine(errorMessage)
			return False
		elif elseCount == 1 and returnValue[-2][1] != '#else':
			errorMessage = "ERROR in checkPreprocessingDirectivesInterleaving() - the #else statement must be the penultimate one"
			errorRoutine(errorMessage)
			return False

	# The returnValue is an array of [lineNumber,ifthenelseendif]
	return returnValue

########################################################################################################
# The reason we made it a separate routine is because we will have to call it every time we
# include a file.
########################################################################################################	
def removeComments():
	global lines
	# Remove single-line comments
	i = 0
	while i < len(lines):
		if "//" in lines[i]:			
			lines[i] = lines[i][:lines[i].find("//")]
		i+= 1
	PRINT (lines )
	#PRINT ("len(lines) = ", len(lines) )
	
	# Remove Multi-line comments
	commentStartLineIndex = -1000	#Something illegal value
	commentStartCharIndex = -1000	#Something illegal value
	i = 0
	ongoingComment = False
	#TO-DO: Change the code so that commentEndCharIndex is indeed the last char # of the comment, not the char AFTER that
	while i < len(lines):
		# End a previously running comment
		if ongoingComment == True and "*/" not in lines[i]:
			lines[i]= ""			# Delete whole line; comment still continues
		else:
			if ongoingComment == True and "*/" in lines[i]:
				commentEndCharIndex = lines[i].index("*/")+1
				if i > commentStartLineIndex:
					lines[i]=lines[i][commentEndCharIndex+1:]
					ongoingComment = False
			if ongoingComment == False:
				while "/*" in lines[i] and "*/" in lines[i] and (lines[i].index("/*")+2 <=lines[i].index("*/")):	# make sure we do not count /*/ as a valid comment
					commentStartCharIndex = lines[i].index("/*")
					commentEndCharIndex = lines[i].index("*/")+1
					lines[i]=lines[i][:commentStartCharIndex]+lines[i][commentEndCharIndex+1:]
				if 	"/*" in lines[i]:
					ongoingComment = True
					commentStartCharIndex = lines[i].index("/*")
					lines[i]=lines[i][:commentStartCharIndex]
		i+= 1
	return

########################################################################################################
# The reason we made it a separate routine is because we will have to call it every time we
# include a file.
########################################################################################################	
def condenseMultilineMacroIntoOneLine():
	global lines
	# Handle multi-line macros to make them a single line
	#PRINT ("======================\nGoing to handle multi-line macros\n======================" )
	PRINT ("len(lines) = ", len(lines) )
	i = 0
	while i < len(lines):
		PRINT ((" line # %d = <%s>" % (i,lines[i])) )
		i = i+1
		
	i = 0
	ongoingMacro = False
	while i < len(lines):
		#PRINT ("searching for macro in", lines[i] )
		currLine = lines[i].strip()					# TO-DO: This could be a problem if a string liternal spans over multiple lines and any such line ends with a space
		if re.search("^#define\s+.+", currLine): 
			ongoingMacro = True
			macroFoundInLine = i
			while currLine[-1:] == "\\":
				PRINT (("Found backslash at the end of currLine =<%s>" % currLine) )
				i = i+1
				if i < len(lines):
					PRINT ("Multiline macro extends to line # ", i )
					PRINT (("currLine = <%s>, currLine[:-1] = <%s>, lines[i].strip() = <%s>" % (currLine , currLine[:-1] , lines[i].strip())) )
					currLine = currLine[:-1] + lines[i].strip()
					lines[i] = ""
				else:
					PRINT ("ERROR  in condenseMultilineMacroIntoOneLine() - missing multi-line macro - Exiting!" )
					return False
					sys.exit()
			ongoingMacro = False
			lines[macroFoundInLine] = currLine
		i=i+1	
	return True
	
#MUST_PRINT(parseArithmeticExpression(['a',',','b',',','c',',','d']))
#sys.exit()

############################################################################
#  1. PROCESS COMMENTS                                                     #
#  2. CONVERT MULTI-LINE MACROS INTO SINGLE-LINE MACROS                    #
#  3. HANDLE include "filename" STATEMENTS                                 #
#                                                                          #
#  THIS function HAPPENS BEFORE (AND WITHOUT) TOKENIZING THE lines.        #
#  HOWEVER, WITHIN THIS FUNCTION, WE DO TOKENIZE EVERY LINE.               #
#                                                                          #
#  One note of caution. Do not use something like currLine in this routine,#
#  since the currLine is always getting updated. Use lines[i] always.      #
############################################################################
def preProcess():
	global lines, defsByLines, PRINT_DEBUG_MSG
	
	
	if not lines:
		PRINT ("ERROR in preProcess - the code lines cannot be empty - exiting" )
		return False
		sys.exit()
	else:
	
#	InputCodeFile = r"InputStructure.txt"
#	with open(InputCodeFile, 'r') as f:
#		lines = f.readlines()
		PRINT (lines )
		PRINT ("len(lines) = ", len(lines) )
		
				
		PRINT ("======================\nGoing to handle preprocessor directives\n======================" )
		PRINT ("lines =",lines)
		
		defsByLines = []
		# Initialize it to blank TO-DO: We must handle the case of lines expanding due to include statement
		for row in lines:
			defsByLines.append([])

		i=0
		# !!!!! DO NOT REMOVE THIS LINE BELOW !!!!!
		#while i < len(lines):	#Left for showing bug. since the lines will potentially expand after processing <include "filename"> statement, len(lines) is not constant
		while True:
			if i >= len(lines):
				break
		
			# First thing you do is inherit all the available definitions by this line from the previous line
			if i>0:
				defsByLines[i] = defsByLines[i-1]
		
			# KLUDGE
			#The very first thing you do to remove any whitespace to the left of right of a # when the line begins with a #
			#TO-DO: This will fail when we have a multi-line string where a middle line starts with # (Bug)
			#The only way to do it cleanly is to separate ALL the preprocessor tokens (like '#define') into two tokens (like '#' followed by 'define')
			if re.match('^\s+#\s*',lines[i]) or re.match('^\s*#\s+',lines[i]):
				PRINT("Before stripping the whitespace around the beginning # for line # %d <%s> "%(i,lines[i]))
				lines[i] = re.sub('^\s*#\s*','#',lines[i])
				PRINT("After  stripping the whitespace around the beginning # for line # %d <%s> "%(i,lines[i]))

			# Remove Multi-line comments
			removeComments()
			
			# Condense each Multi-line Macro into a single-line macro 
			status = condenseMultilineMacroIntoOneLine()
			if status == False:
				errorMessage = "ERROR in preProcess() after calling condenseMultilineMacroIntoOneLine()"
				errorRoutine(errorMessage)
				return False

			#PRINT ("searching for macro definitions in line # ",i, lines[i] )
			currLine = lines[i]
			PRINT("lines[",i,"] =",lines[i])

			tokenizeLinesResult = tokenizeLines(lines[i])
			PRINT("tokenized lines[",i,"] =",tokenizeLinesResult)
			
			if tokenizeLinesResult == False:
				PRINT ("ERROR in preProcess after calling tokenizeLines(currLine) for currLine =",lines[i] )
				return False
			else:
				currLineTokenList = tokenizeLinesResult[0]

			#preprocessingDirectives = ('#include', '#if', '#ifdef', '#ifndef', '#else', '#elif', '#endif', '#define', '#undef', '#line', '#error', '#pragma')

			if currLineTokenList and currLineTokenList[0] in preprocessingDirectives:
				PRINT("currLineTokenList[0] =",currLineTokenList[0],"is a preprocessingDirectives")
				
				# Handle the include statements
				if currLineTokenList[0] == '#include':
					if len(currLineTokenList) != 2 and len(currLineTokenList) != 4:
						errorMessage = "ERROR in preProcess() after calling tokenizeLines() for line # %d = <%s> - #include must have exactly one arguement" %(targetLineNumber,lines[targetLineNumber] )
						errorRoutine(errorMessage)
						return False
					elif len(currLineTokenList) == 4 and not (currLineTokenList[1] == '<' and currLineTokenList[3] == '>') and not (currLineTokenList[1] == '"' and currLineTokenList[3] == '"'):
							errorMessage = "ERROR in preProcess() after calling tokenizeLines() for line # %d = <%s> - must be like #include <filename>" %(targetLineNumber,lines[targetLineNumber] )
							errorRoutine(errorMessage)
							return False
					elif len(currLineTokenList) == 2 and (currLineTokenList[1][0] != '"' or currLineTokenList[1][-1] != '"' or len(currLineTokenList[1])<=2):
							errorMessage = "ERROR in preProcess() after calling tokenizeLines() for line # %d = <%s> - must be like #include \"filename\"" %(targetLineNumber,lines[targetLineNumber] )
							errorRoutine(errorMessage)
							return False
					else: 
						includedFileName = currLineTokenList[1][1:-1].strip() if len(currLineTokenList) == 2 else currLineTokenList[2]
						if not includedFileName:
							errorMessage = "ERROR in preProcess() - included filename cannot be blank"
							errorRoutine(errorMessage)
							return False
							
						PRINT("includedFileName =",includedFileName)
						slash = "\\" if "\\" in os.getcwd() else "/" if "/" in os.getcwd() else ""
						includeFilePaths = returnFilePathList(INCLUDE_FILE_PATHS)
						fileFound = False
						if os.path.exists(includedFileName):
							path = os.getcwd()
							path = path if path[-1] == slash else path+slash
							fileFound = True
							PRINT("The file",includedFileName,"is present in the current working directory",path)
						elif includeFilePaths != False and includeFilePaths != []:
							for item in includeFilePaths:
								if not checkIfString(item) or item[-1]!=slash:
									errorMessage = "ERROR in preProcess() - included file path <%s> is illegal"%(STR(item))
									errorRoutine(errorMessage)
									return False
								if os.path.isfile(item+includedFileName):
									path = item
									fileFound = True
									PRINT("The file",includedFileName,"is present in the include file path",path)
									break
						if fileFound:
							with open(path+includedFileName, "r") as includedFile:
								try:
									includedLines = includedFile.readlines()
									if not checkIfStringOrListOfStrings(includedLines):
										errorMessage = "ERROR in coding: input code file content is NOT string - type(includedLines) = "+STR(type(asciiLines))
										errorRoutine(errorMessage)
										return False
									
								except ValueError: # Empty file
									includedLines = [""]
						else:
							OUTPUT("ERROR - cannot open included code file",includedFileName)
							sys.exit()
							
						PRINT ("Included code file has",len(includedLines),"lines, which contains:", includedLines )
						PRINT ("Before inserting, len(lines) =",len(lines))
						
						# Insert the newly included lines in lines; also update the defsByLines
						tempLines = lines[:i]
						tempDefsByLines = defsByLines[:i+1]	# not a typo (we need to keep the inheritance from line # i-1)
						
						tempLines.extend(includedLines)
						for j in range(len(includedLines)-1):
							tempDefsByLines.append([])
							
						if i<len(lines)-1:
							tempLines.extend(lines[i+1:])
							tempDefsByLines.extend(defsByLines[i+1:])
								
						lines = tempLines
						defsByLines = tempDefsByLines
						PRINT ("After inserting, len(lines) =",len(lines), "len(defsByLines) =",len(defsByLines))
						if len(lines) != len(defsByLines):
							errorMessage = "ERROR in preProcess(): len(lines) (%d) != len(defsByLines) (%d)"%(len(lines), len(defsByLines))
							errorRoutine(errorMessage)
							return False
								

				elif currLineTokenList[0] == '#error':
					warningMessage = "This tool currently ignores all #error statements: <"+lines[i]+">"
					warningRoutine(warningMessage)
				elif currLineTokenList[0] == '#line':
					warningMessage = "This tool currently ignores all #line statements: <"+lines[i]+">"
					warningRoutine(warningMessage)
				elif currLineTokenList[0] in ('#if','#ifdef','#ifndef','#elif'):
				
					# First figure out the which all source code statements are impacted by this if statement.
					# There might be multiple code blocks between the if-elif-elif-else-endif statements, but only one of them would succeed.
					checkPreprocessingDirectivesInterleavingResult = checkPreprocessingDirectivesInterleaving(lines[i:])
					if checkPreprocessingDirectivesInterleavingResult == False:
						errorMessage = "ERROR in preProcess() after calling checkPreprocessingDirectivesInterleaving() from line %i"%i
						errorRoutine(errorMessage)
						return False
					else:
						scope = checkPreprocessingDirectivesInterleavingResult

					PRINT("For line #",i," the scope for the if-elif-else-endif is",scope)
					
					# Recall that the the line numbers returned from checkPreprocessingDirectivesInterleaving() are relative, i.e. they start from 0.
					# So, you need to add the current line number to get any absolute line number
					k = 0

					# Out of the many if-elif-elif-else-endif code blocks, only one will succeed. And once that succeeds, the rest must be deleted irrespecive of
					# whether corresponding #elif condition evaluates to True or not
					ifConditionTruthValueAlreadyFound = False
					
					while k<len(scope):
						targetLineNumber = scope[k][0]+i
						PRINT("Tokenizing line #",targetLineNumber)

						deleteCodeBlock = False
						
						# If we already had one of the if-elif-elif-else-endif condition
						if ifConditionTruthValueAlreadyFound:
							deleteCodeBlock = True
						else:
							PRINT("Going to tokenizeLines(\"",lines[targetLineNumber],"\")")
							tokenizeLinesResult = tokenizeLines(lines[targetLineNumber])
							if tokenizeLinesResult == False:
								errorMessage = "ERROR in preProcess() after calling tokenizeLines() for line # %d = <%s>" %(targetLineNumber,lines[targetLineNumber] )
								errorRoutine(errorMessage)
								return False
							else:
								PRINT("tokenizeLinesResult =",tokenizeLinesResult)
								targetLineTokenList = tokenizeLinesResult[0]
					
							if targetLineTokenList[0] in ('#if','#ifdef','#ifndef', '#elif') and len(targetLineTokenList)<2:
								errorMessage = "ERROR in line #"+targetLineNumber+": an "+ targetLineTokenList[0] +" statement must not be empty"
								errorRoutine(errorMessage)
								return False
							elif targetLineTokenList[0] in ('#ifdef','#ifndef') and len(targetLineTokenList)>2:
								errorMessage = "ERROR in line #"+targetLineNumber+": an "+ targetLineTokenList[0] +" statement must not supply more than one argument"
								errorRoutine(errorMessage)
								return False
							elif targetLineTokenList[0] in ('#else','#endif') and len(targetLineTokenList)>1:
								errorMessage = "ERROR in line #"+targetLineNumber+": an "+ targetLineTokenList[0] +" statement must not supply more than one argument"
								errorRoutine(errorMessage)
								return False
							
							# Calculate the if condition result (True or False)
							ifConditionEvaluationResult = False	# The default value

							if targetLineTokenList[0] == '#else': 	# If you are falling on an #else, it is by defintion true
								ifConditionEvaluationResult = True
								PRINT("The '#else' succeeded")
							elif targetLineTokenList[0] == '#ifdef': 
								if targetLineTokenList[1] in defsByLines[i]:
									ifConditionEvaluationResult = True
									PRINT("The '",targetLineTokenList[0],targetLineTokenList[1],"' succeeded")
								else:
									PRINT("The '",targetLineTokenList[0],targetLineTokenList[1],"' failed")
							elif targetLineTokenList[0] == '#ifndef': 
								if targetLineTokenList[1] not in defsByLines[i]:
									ifConditionEvaluationResult = True
									PRINT("The '",targetLineTokenList[0],targetLineTokenList[1],"' succeeded")
								else:
									PRINT("The '",targetLineTokenList[0],targetLineTokenList[1],"' failed")
							elif targetLineTokenList[0] in ('#if','#elif'):
								
								# Handle one special case - before calling parseArithmeticExpression(), we must resolve the case of defined().
								# This is because parseArithmeticExpression() is agnostic of exactly where in the source file the code is,
								# but the result of a defined(symbol) depends precisely on that. So parseArithmeticExpression() cannot
								# figure that out. So, we handle it locally first. We relace the defined(symbol) with 1 or 0.
								
								if 'defined' in targetLineTokenList:
									currLineTokenListTransformed = targetLineTokenList
									while True:
										if 'defined' in currLineTokenListTransformed:
											definedIndex = currLineTokenListTransformed.index('defined')
											if definedIndex +3 < len(currLineTokenListTransformed) and currLineTokenListTransformed[definedIndex+1] == '(' and currLineTokenListTransformed[definedIndex+3] == ')':
												symbolToCheckIfDefined = currLineTokenListTransformed[definedIndex+2]
												#replace the 'defined' token with 1 or 0, and delete the three subsequent tokens signifying (symbol)
												PRINT("Looking for Symbol", symbolToCheckIfDefined,"in defsByLines[",i,"] =",STR(symbolToCheckIfDefined))
												if symbolToCheckIfDefined in defsByLines[i]:
													currLineTokenListTransformed[definedIndex] = '1'
													PRINT("Found it - replacing defined(",symbolToCheckIfDefined,") with 1")
												else:
													currLineTokenListTransformed[definedIndex] = '0'
													PRINT("Did not find it - replacing defined(",symbolToCheckIfDefined,") with 0")
												del currLineTokenListTransformed[definedIndex+1:definedIndex+4]
										else:
											break
									targetLineTokenList = currLineTokenListTransformed
									
							
								parseArithmeticExpressionResult = parseArithmeticExpression(targetLineTokenList[1:])
								if parseArithmeticExpressionResult == False:
									errorMessage = "ERROR in preProcess() parsing <%s>"%tokenizeLinesResult
									errorRoutine(errorMessage)
									return False
									
								evaluateArithmeticExpressionResult = evaluateArithmeticExpression(parseArithmeticExpressionResult)
								PRINT("evaluateArithmeticExpression(",STR(parseArithmeticExpressionResult),") evaluates to", evaluateArithmeticExpressionResult)
								if evaluateArithmeticExpressionResult[0] == False:
									errorMessage = "ERROR in preProcess() evaluating <%s>"%evaluateArithmeticExpressionResult
									errorRoutine(errorMessage)
									return False
								elif evaluateArithmeticExpressionResult[1] == 1:	# Truth value in C is 1, not True of Python
									ifConditionEvaluationResult = True
								elif evaluateArithmeticExpressionResult[1] == 0:	# False value in C is 0, not False of Python
									ifConditionEvaluationResult = False
								else:
									errorMessage = "ERROR in preProcess() evaluating <%s> - it is not 1 or 0"%evaluateArithmeticExpressionResult
									errorRoutine(errorMessage)
									return False
									
								if ifConditionEvaluationResult == True:
									PRINT("The if condition in line#",targetLineNumber," = <",lines[targetLineNumber],"> succeeded")
								else:
									PRINT("The if condition in line#",targetLineNumber," = <",lines[targetLineNumber],"> failed")

							if ifConditionEvaluationResult == True:
								ifConditionTruthValueAlreadyFound = True
								PRINT("The overall if condition in line#",targetLineNumber," = <",lines[targetLineNumber],"> succeeded")
							else:
								PRINT("The overall if condition in line#",targetLineNumber," = <",lines[targetLineNumber],"> failed")
								deleteCodeBlock = True
							
							
						# Now that we have calculated the if condition result (True or False), delete the if statements and corresponding non-executing code blocks
						if not deleteCodeBlock or k == len(scope)-1:
							numLinesToDelete = 1
						else:
							numLinesToDelete = scope[k+1][0] - scope[k][0]
							
						PRINT ("Going to delete line",scope[k][0]+i,"through line",scope[k][0]+i+numLinesToDelete-1," - a total of",numLinesToDelete,"lines" )
						d = 0
						while d < numLinesToDelete:
							lines[scope[k][0]+i+d] = ""
							if d > 0:	# For all the lines except the first
								defsByLines[scope[k][0]+i+d] = defsByLines[targetLineNumber]
							d += 1
						k += 1
					
#		PRINT ("======================\nGoing to handle expansions of macros\n======================" )
			
			# TO-DO: Handle the case that the #define does not ooccur inside a string literal. 
			# For example, a statement like String1 = "No #define here" should not invoke macro processing
#			if re.search("^\s*#define\s+.+", currLine):	# What if the #define is the only thing that is on that line?
			if re.search("^\s*#define\s*", lines[i]):
				#  Each row of this macros table will have 3 parts: macroName, argumentList, macroExpansionText
				# (Recall that multi-line macros have alredy been converted to single-line macros).
				# Find out if this macro takes parameters or not. Remember that by now ALL multi-line macros have already been converted to single-line macros
				macroTokenListResult = tokenizeLines(lines[i])
				if macroTokenListResult == False:
					PRINT ("ERROR in preProcess after calling tokenizeLines(currLine) for currLine =",lines[i] )
					return False
				else:
					macroTokenList = macroTokenListResult[0]
					
				if macroTokenList[0] != "#define" :
					PRINT ("ERROR in preProcess() - Unknown token", macroTokenList[0], " -- exiting!" )
					return False
					sys.exit()
				elif len(macroTokenList) < 2:
					PRINT ("ERROR in preProcess() - Macro must have a valid name" )
					errorMessage = "ERROR in line <%s> - Macro must have a valid name -- exiting!"%lines[i]
					errorRoutine(errorMessage)
					return False
					sys.exit()
				elif not re.search("^\s*[a-zA-Z_]+\w*", macroTokenList[1]):
					PRINT ("ERROR in preProcess() - Macro must have a valid name", macroTokenList[1], " -- exiting!" )
					return False
					sys.exit()
				
				macroName = macroTokenList[1]
				
				# Add this macroName to the definitions available
				PRINT("For line #",i,", current available definitions are",defsByLines[i])
				if macroName not in defsByLines[i]:
					PRINT("Adding", macroName,"to this list")
					defsByLines[i].append(macroName)
				else:
					PRINT("No need to add", macroName,"to this list since it already exists there")
				
				#TO-DO: Need to check that the macroName is NOT a keyword
				# currLine
				# First handle the case that the macro takes no arguments
				if re.search("^\s*#define\s+[a-zA-Z_]+\w*\s*$", lines[i]) or re.search("^\s*#define\s+[a-zA-Z_]+\w*\s+\S*", lines[i]):
					PRINT ("Macro ", macroName,"takes NO arguments" )
					# First handle the case that the macro resolves to NULL
					if re.search("^\s*#define\s+[a-zA-Z_]+\w*\s*$", lines[i]):
						macroExpansionText = ""
					elif re.search("^\s*#define\s+[a-zA-Z_]+\w*\s+\S*", lines[i]):
						# Find the expansion text
						macroExpansionText = re.sub("^\s*#define\s+%s\s+"% macroName,"", lines[i])
					PRINT (("Macro <%s> expands to <%s>"%(macroName,macroExpansionText)) )
					# replace the macro invocation with all subsequent lines
					j=i+1
					while j<len(lines):
						# There are some macro invocations that we are not supposed to replace. To make sure we don't hit them again and again, 
						# this index below always moves forward.
						checkForMacroFromTokenIndex = 0
						while True:
							tokenizeLinesOutputResult = tokenizeLines(lines[j])
							if tokenizeLinesOutputResult == False:
								PRINT ("ERROR in after calling tokenizeLines(lines[j]) for lines[",j,"] =", lines[j] )
								return False
							else:
								tokenizeLinesOutput = tokenizeLinesOutputResult[0]
							
							# We have the problem that we are NOT supposed to replace the macroname in some very special cases (like #ifdef etc.)
							# But, if you just keep checking if macroName in full tokenizeLinesOutput, you will always get a false hit for those special cases, 
							# since those matches are never going to be replaced.
							# So, we need an alternative approach. Every time we get a hit, we only check from the susequent token in the next run.
							if checkForMacroFromTokenIndex<len(tokenizeLinesOutput) and macroName in tokenizeLinesOutput[checkForMacroFromTokenIndex:]: 
							
								macroNameFoundAtIndex = checkForMacroFromTokenIndex+tokenizeLinesOutput[checkForMacroFromTokenIndex:].index(macroName)
								# Do not replace it if it is a #undef(macroName) / #ifdef(macroName) / #ifndef(macroName), or a defined(macroName) in a #if statement
								if tokenizeLinesOutput[0] in ('#undef', '#ifdef', '#ifndef'):
									checkForMacroFromTokenIndex = macroNameFoundAtIndex+1
									PRINT("Found", macroName,"at token index",macroNameFoundAtIndex)
									if checkForMacroFromTokenIndex != 2:
										PRINT("Which is an error")
										sys.exit()
									continue
								elif tokenizeLinesOutput[0] in ('#if') and tokenizeLinesOutput[macroNameFoundAtIndex-2]=='defined' and tokenizeLinesOutput[macroNameFoundAtIndex-1]=='(' and tokenizeLinesOutput[macroNameFoundAtIndex+1]==')' :
									checkForMacroFromTokenIndex = macroNameFoundAtIndex+2
									PRINT("Found", macroName,"at token index",macroNameFoundAtIndex,", as part of",tokenizeLinesOutput[macroNameFoundAtIndex-2:macroNameFoundAtIndex+2])
									continue
								
								PRINT ("BEFORE invoking macro", macroName, "line #",j," = <",lines[j],">" )
								macroInvocationLocation = findTokenListInLines(lines[j],macroName)
								if macroInvocationLocation == False:
									PRINT ("ERROR after calling findTokenListInLines(lines[j],macroName) for lines[",j,"] = ",lines[j]," and macroName =",macroName )
									return False
								elif macroInvocationLocation[1] != 0 or macroInvocationLocation[3] != 0 or lines[j][macroInvocationLocation[2]:macroInvocationLocation[4]+1] != macroName:
									PRINT ("ERROR in preProcess() - the match must happen within current line, while its occurrence location is", macroInvocationLocation )
									PRINT ("and the lines[",j,"][",macroInvocationLocation[2],":",macroInvocationLocation[4]+1,"] = <",lines[j][macroInvocationLocation[2]:macroInvocationLocation[4]+1],">, while macroName = <",macroName,">" )
									return False
									sys.exit()
								else:
									
									PRINT ("The macro", macroName,"appears in line #",j+macroInvocationLocation[1],"char #",macroInvocationLocation[2] )
									lines[j] = lines[j][:macroInvocationLocation[2]]+macroExpansionText+lines[j][macroInvocationLocation[4]+1:]
	#								lines[j]=re.sub(macroName,macroExpansionText,lines[j])
									PRINT ("AFTER invoking macro", macroName, "line #",j," = <",lines[j],">" )
									runWhileLoopAgain = True
							else:
								break
						j=j+1
						
				# Next handle the case that the macro takes arguments (where there is no gap between the macro name and the following parenthesis)
				elif re.search("^#define\s+[a-zA-Z_]+\w*\(", lines[i]):
				
					variadicMacro = False
					variadicMacroExplicitArgumentCount = 0
					variadicMacroArgSpecialName = ""
				
					PRINT ("Macro ", macroName,"takes arguments" )
					temp = re.sub("^\s*#define\s+[a-zA-Z_]+\w*\(", "",lines[i])	# Keep in mind that the temp is missing the first '(' of the argument list
					PRINT ("temp = <",temp,">" )
					# There cannot be nested parenthesis inside the argument list for macro  definition (it is allowed during invocation, but not during definition)
					if ")" not in temp:
						PRINT ("ERROR in preProcess() - No ending parenthesis for macro argument list - exiting!" )
						return False
						sys.exit()
					else:
						endParenthesis = temp.index(')');
						if "(" in temp:
							newBeginParenthesis = temp.index('(');
							if newBeginParenthesis < endParenthesis:
								PRINT ("ERROR in  preProcess() : \"\(\" may not appear in macro parameter list" )
								return False
								sys.exit()
						macroArgumentsDefined = "("+temp[:endParenthesis]+")"
						tokenizeLinesOutputResult = tokenizeLines(macroArgumentsDefined)
						if tokenizeLinesOutputResult == False:
							PRINT ("ERROR - exiting because tokenizeLines(macroArgumentsDefined) = False where macroArgumentsDefined =",macroArgumentsDefined )
							return False
						else:
							tokenizeLinesOutput = tokenizeLinesOutputResult[0]
							if tokenizeLinesOutput[0] != '(' or tokenizeLinesOutput[-1] != ')':
								errorMessage = "Illegal argument list for macro %s: %s"%(macroName, STR(tokenizeLinesOutput))
								errorRoutine(errorMessage)
								return False
							
						# Variadic macros - check its input argument list format. Valid formats are ([arg1, arg2,...,argn,][specialName] ...)
						if tokenizeLinesOutput[-2]=='...':
							variadicMacro = True
							PRINT("Variadic macro found")
							if tokenizeLinesOutput[-3]!=',' and tokenizeLinesOutput[-3]!='(' : # We have a case like #define MacroName(args ...)
								variadicMacroArgSpecialName = tokenizeLinesOutput[-3]
								PRINT("Variadic macro argument it is referenced as",tokenizeLinesOutput[-3])
								PRINT("Now deleting this ... token from tokenizeLinesOutput =",tokenizeLinesOutput)
								del tokenizeLinesOutput[-2]	
								PRINT("After deleting", variadicMacroArgSpecialName, ", tokenizeLinesOutput =",tokenizeLinesOutput)
							else:
								tokenizeLinesOutput[-2] = '__VA_ARGS__'	# We do this so that in the expansion we can simply do regular replacements
							
							numTokensUnconsumed = len(tokenizeLinesOutput)-3
							if numTokensUnconsumed %2 != 0:
								errorMessage = "Illegal argument list for macro %s: %s"%(macroName, STR(tokenizeLinesOutput))
								errorRoutine(errorMessage)
								return False
							variadicMacroExplicitArgumentCount = integerDivision(numTokensUnconsumed,2)
							for t in range(variadicMacroExplicitArgumentCount):
								if tokenizeLinesOutput[2*(t+1)] != ',' or tokenizeLinesOutput[2*(t+1)-1] == ',':	# Recall that the tokenizeLinesOutput[0] = '('
									errorMessage = "Illegal argument list for macro %s: %s"%(macroName, STR(tokenizeLinesOutput))
									errorRoutine(errorMessage)
									return False
							PRINT("There are", variadicMacroExplicitArgumentCount,"explicit arguments before the ... in this variadic macro")
							
							
						# Remember that for variadic macros with a special name for ... , we have deleted that token	
						argumentList = parseArgumentList(tokenizeLinesOutput)
						if argumentList == False:
							PRINT ("Exiting - Error parsing for arguments in tokenized version of",macroArgumentsDefined )
							return False
							sys.exit()
						PRINT ("The macro",macroName,"takes the following argument list:",argumentList )
						PRINT ("We have used argumentList = parseArgumentList(\"(\"+temp[:endParenthesis]+\")\"). If we had used argumentList = re.sub(\"\s*\",\"\",temp[:endParenthesis]).split(\",\"), then we would have gotten" )
						PRINT (re.sub("\s*","",temp[:endParenthesis]).split(","))	# Remove all the whitespace from the argumentlist first, and then split it 
						# argumentList = parseArgumentList("("+temp[:endParenthesis]+")")
						# Check that there are no repeated arguments. For example, we cannot have a macro like #define func1(a,b,a). All arguments must be unique
						argIndexI = 0
						while argIndexI < len(argumentList):
							argIndexJ = argIndexI + 1
							while argIndexJ < len(argumentList):
								if argumentList[argIndexI] == argumentList[argIndexJ]:
									PRINT ("ERROR  in preProcess() - Macro", macroName, "has repeated argument, argumentList[",argIndexI,"] =",argumentList[argIndexI], "is same as argumentList[",argIndexJ,"]=", argumentList[argIndexJ] )
									return False
									sys.exit()
								argIndexJ = argIndexJ + 1
							argIndexI = argIndexI + 1	

						PRINT("The argument list for this macro is valid")
						
						# TO-DO: Can we have a case like where macro expansion text contains a quoted string literal that spills over to the next line?
						macroExpansionText = temp[endParenthesis+1:].strip()
						PRINT ("The macro",macroName,"expands into: <",macroExpansionText,">" )
						tokenizeLinesOutputResult = tokenizeLines(macroExpansionText)
						if tokenizeLinesOutputResult == False:
							PRINT ("Exiting - tokenizeLines(macroExpansionText) = False for macroExpansionText =",macroExpansionText )
							return False
						else:
							tokenizeLinesOutput = tokenizeLinesOutputResult[0]
							
						if variadicMacro and variadicMacroArgSpecialName and '__VA_ARGS__' in tokenizeLinesOutput:
							errorMessage = "When we use a special symbol (%s) instead of the '...' for a variadic macro, the macro expansion text (%s) can no longer have '__VA_ARGS__' in it"%(variadicMacroArgSpecialName, list2plaintext(tokenizeLinesOutput))
							errorRoutine(errorMessage)
							return False
							
						macroExpansionTextAST = parseArithmeticExpression(tokenizeLinesOutput)
						if macroExpansionTextAST == False:
							PRINT ("ERROR after calling parseArithmeticExpression(tokenizeLinesOutput) for tokenizeLinesOutput =",tokenizeLinesOutput )
							return False
							sys.exit()
						else:
							PRINT ("============================\nmacroExpansionTextAST = \n", macroExpansionTextAST )

						# For variadic macros, when the macro expansion has special terms like __VA_OPT__(things) and ##__VA_ARGS__, 
						# special things happen when the __VA_ARGS__ part turns out to be null.
						#
						# For __VA_OPT__(things), the things part become omitted from the macro expansion when the __VA_ARGS__ part turns out to be null.
						# for ##__VA_ARGS__, the preceding comma is omitted if __VA_ARGS__ turns out to be null.
						#
						# So, for variadic macros with __VA_OPT__(things) and ##__VA_ARGS__ and when __VA_ARGS__ is indeed null, there is an alternative macro expansion.
						
						temp = tokenizeLinesOutput
						
						token__VA_ARGS__ = variadicMacroArgSpecialName if variadicMacroArgSpecialName else '__VA_ARGS__'
						
						PRINT("Before handling ## __VA_ARGS__, tokenizeLinesOutput for macro expansion text =",temp)
						while True:
							findIndex = findIndexOfSequenceInList([',','##',token__VA_ARGS__],temp) 
							if findIndex >= 0:
								del temp[findIndex:findIndex+3]
							else:
								break
						PRINT("After handling ## __VA_ARGS__, tokenizeLinesOutput for macro expansion text =",temp)
								
						while True:
							findIndex = findIndexOfSequenceInList(['__VA_OPT__','('],temp) 
							if findIndex >= 0:
								d = matchingBraceDistance(temp[findIndex+1:])
								if d < 0:
									errorMessage = "ERROR in preProcess - no matching ) for __VA_OPT__"
									errorMessage(errorRoutine)
									return False
								del temp[findIndex:findIndex+1+d+1]
							else:
								break
								
						if '__VA_OPT__' in temp:
							errorMessage = "ERROR in preProcess - illegal __VA_OPT__"
							errorMessage(errorRoutine)
							return False
						
						PRINT("After handling __VA_OPT__(), tokenizeLinesOutput for macro expansion text =",temp)

						while True:	# There still might be some __VA_ARGS__ without any preceding ## or __VA_OPT__
							findIndex = findIndexOfSequenceInList([token__VA_ARGS__],temp) 
							if findIndex >= 0:
								del temp[findIndex]
							else:
								break
						PRINT("After blanking out all other  __VA_ARGS__, tokenizeLinesOutput for macro expansion text =",temp)
						
						null__VA_ARGS__tokenizeLinesOutput = temp

						null__VA_ARGS__macroExpansionTextAST = parseArithmeticExpression(null__VA_ARGS__tokenizeLinesOutput)
						if null__VA_ARGS__macroExpansionTextAST == False:
							OUTPUT ("ERROR after calling parseArithmeticExpression() for null__VA_ARGS__tokenizeLinesOutput =", null__VA_ARGS__tokenizeLinesOutput)
							return False
							sys.exit()
						else:
							PRINT ("============================\nnull__VA_ARGS__macroExpansionTextAST = \n", null__VA_ARGS__macroExpansionTextAST )
						
						# So, after all these, we use the following method.
						# - If the macro is variadic and __VA_ARGS__ is null, use null__VA_ARGS__macroExpansionTextAST.
						# - For all other cases, use macroExpansionTextAST.
						
						# replace the macro invocation with all subsequent lines
						j=i+1
						while j<len(lines):
							# TO-DO: A single might have multiple invocations of the same macroName, so need to put it in a while loop
#							macroInvocationLineTokenized = tokenizeLines(lines[j])
							# TO-DO: Handle the case of multiple invocations of the same macro in a single line
							# MannaManna - is it even valid syntax for python???
							while tokenizeLines(lines[j]) != False and macroName in tokenizeLines(lines[j])[0]: # Do not use simple string matching, because the macroName might appear part of a literal or a string
								macroInvocationLineTokenizedResult = tokenizeLines(lines[j])
								if macroInvocationLineTokenizedResult == False:
									PRINT ("Exiting - Error tokenizing lines[",j,"] = ",lines[j] )
									return False
								else:
									macroInvocationLineTokenized = macroInvocationLineTokenizedResult[0]
									
								macroInvokedTokenIndex = macroInvocationLineTokenized.index(macroName)
								PRINT ("Found macro-with-argument <",macroName,"> in line #",j,"=<",lines[j],">, which has been tokenized as",macroInvocationLineTokenized )
								PRINT ("The macro invocation is at token #", macroInvokedTokenIndex )
								# We do this because the parseArithmeticExpression routine expects the function name
								# If we just give the (A, B, C) kind of text instead of the expected func(A, B, C), it might error out
								macroExpansionScope = macroName		
								MacroParametersFound = False
								k = j
								macroNamePosition = findTokenListInLines(lines[k:],macroName)
								if macroNamePosition == False:
									PRINT ("ERROR after calling findTokenListInLines(lines[k:],macroName) for lines[",k,":] =", lines[k:], " and macroName =",macroName )
									return False
								PRINT ("Macro", macroName," found at",macroNamePosition," relative to line #" ,k )
								if (macroNamePosition[0] < 0 or macroNamePosition[1] != 0 or macroNamePosition[2] < 0 or macroNamePosition[2] >= len(lines[k]) or 
										  					    macroNamePosition[3] != 0 or macroNamePosition[4] < 0 or macroNamePosition[4] >= len(lines[k])): #Shouldn't happen
									PRINT ("ERROR in preProcess() - weird error - Apparently no match for macro", macroName,"in line #",k," = ",lines[k] )
									return False
									sys.exit()
								elif macroNamePosition[2] == 0:
									stringBeforeMacroName = ""
								else:
									stringBeforeMacroName = lines[k][:macroNamePosition[2]]
								
								stringAfterMacroName = lines[k][macroNamePosition[4]+1:]
								PRINT ("The stringBeforeMacroName <", macroName, "> = <",stringBeforeMacroName,">, k=",k )
								PRINT ("The stringAfterMacroName <", macroName, "> = <",stringAfterMacroName,">, k=",k )
						
								'''
								# This code below will fail if the macroName occurs inside a string before the actual macro invocation
								# We are just keeping it for some time to ensure that we are getting correct results. Ultimately it will be deleted
								stringBeforeMacroNameAlternate = re.split(macroName,lines[k],1)[0]	# We don't strip since we want to preserve as much of it as possible
								stringAfterMacroNameAlternate  = re.split(macroName,lines[k],1)[1]
								if stringBeforeMacroName != stringBeforeMacroNameAlternate or stringAfterMacroName != stringAfterMacroNameAlternate:
									PRINT ("WARNING - watch out for possible errors" )
									PRINT ("The stringBeforeMacroName          <", macroName, "> = <",stringBeforeMacroName,">" )
									PRINT ("The stringBeforeMacroNameAlternate <", macroName, "> = <",stringBeforeMacroNameAlternate,">" )
									PRINT ("The stringAfterMacroName          <", macroName, "> = <",stringAfterMacroName,">" )
									PRINT ("The stringAfterMacroNameAlternate <", macroName, "> = <",stringAfterMacroNameAlternate,">" )
								'''
								# The macro argument list could be distributed over many lines
								restLines = []
								PRINT ("Currently, lines[%d]=<%s>"%(k,lines[k]) )
								if macroNamePosition[4] < len(lines[k])-1:
#									PRINT ("Appending <%s> to restLines, curretly k=%d"%(lines[k][macroNamePosition[4]+1:],k) )
									restLines.append(lines[k][macroNamePosition[4]+1:])
								lineIndex = k+1
								while lineIndex < len(lines):
#									PRINT ("Appending <%s> to restLines"%lines[lineIndex] )
									restLines.append(lines[lineIndex])
									lineIndex = lineIndex + 1
								
								PRINT ("Now going to tonize restLines = ",restLines )
								invocationTokensResult = tokenizeLines(restLines)	# This contains the parenthesized arguments, plus whatever comes after
								if invocationTokensResult == False:
									PRINT ("Error while tokenizeLines(restLines) where restLines = ", restLines )
									return False
								else:
									invocationTokens = invocationTokensResult[0]
									
								endMatchingBraceDistance = matchingBraceDistance(invocationTokens)	# This tells exactly where the end-brace for the parenthesized arguments occur
								if endMatchingBraceDistance < 1:
									PRINT ("Did not find argument list for macro",macroName,"in line #",j, invocationTokens )
									return False
									sys.exit()
								else:
									invocationTokensArgsOnly = invocationTokens[:endMatchingBraceDistance+1]
									PRINT("invocationTokensArgsOnly = <",invocationTokensArgsOnly,">, which we will parse for splitting the arguments")
									argListInvoked = parseArgumentList(invocationTokensArgsOnly)
									if argListInvoked == False:
										PRINT ("Exiting - ERROR during parsing",invocationTokensArgsOnly,"for arguments" )
										return False
										sys.exit()
									PRINT ("After parsing, the argument list for macro",macroName,"invocation in line #",j,"=", argListInvoked )
									
									# Verify that it matches the macro's argument count
									
									# For variadic Macro, the variable part of argument list might be empty. But any explicit argument must be provided
									if variadicMacro and variadicMacroExplicitArgumentCount > len(argListInvoked):
										errorMessage = "ERROR in preProcess() - len(argListInvoked) =" + STR(len(argListInvoked)) + "< variadicMacroExplicitArgumentCount =" + STR(variadicMacroExplicitArgumentCount)
										erroRoutine(errorMessage)
										return False
									# For non-variadic Macro, the argument list count must match
									elif not variadicMacro and len(argListInvoked) != len(argumentList):
										errorMessage = "ERROR  in preProcess() - len(argListInvoked) =" + STR(len(argListInvoked)) + "!= len(argumentList) =" + STR(len(argumentList) )
										erroRoutine(errorMessage)
										return False
									else:
										macroIsVariadicWithNull__VA_ARGS__ = False
										# If variadic macro, just create a single comma-separated string with all the excess arguments. This will be input 
										if variadicMacro: 
											PRINT("Original",len(argListInvoked),"-member argListInvoked =",STR(argListInvoked))
											
											# Handle a special case - if the code mentions the last argument as NULL like this below, then convert it to a blank string
											#
											#  #define eprintf(format, ...) fprintf (stderr, format, __VA_ARGS__)
											#  eprintf("success!\n", );		// Observe that the coder didn't code it as <eprintf("success!\n");> - there is a comma at the end
											if argListInvoked[-1]==[]:
												argListInvoked[-1] = ''
												PRINT("Which is then changed to",len(argListInvoked),"-member argListInvoked =",STR(argListInvoked))
												
											if variadicMacroExplicitArgumentCount + 1 == len(argListInvoked):
												PRINT("Exactly one argument supplied against __VA_ARGS__ , hence no special processing required")
											elif variadicMacroExplicitArgumentCount == len(argListInvoked):	# The __VA_ARGS__ part is null
												PRINT("Adding a dummy NULL string to be used as a replacement for the __VA_ARGS__")
												argListInvoked.append("")	
												macroIsVariadicWithNull__VA_ARGS__ = True
											else:
												commaSeparated__VA_ARGS__ = ",".join(argListInvoked[variadicMacroExplicitArgumentCount:])
												del argListInvoked[variadicMacroExplicitArgumentCount:]
												argListInvoked.append(commaSeparated__VA_ARGS__)
											PRINT("Transformed",len(argListInvoked),"-member argListInvoked =",STR(argListInvoked))
											if len(argListInvoked) != len(argumentList):
												OUTPUT("ERROR - should never happen")
												sys.exit()
												
										PRINT ("The argument count (",len(argumentList),") is acceptable" )
										
										# Now replace the macro expansion AST
										
										PRINT ("\n\n\n=============================================================\nCreating the replacement dictionary")
										argumentInvocationDictionary = OrderedDict()
										for argIndex in range(len(argumentList)):
											# TO-DO: Here is a question - do we replace it with the literal, or the AST version of it?
											# Problem - there is no guarantee that a parameter passed to a macro will be a properly formed AST
											argInvokedAST = parseArithmeticExpression(argListInvoked[argIndex])
											if argInvokedAST == False:
												errorMessage = "ERROR after calling parseArithmeticExpression(argListInvoked[argIndex]) for argListInvoked["+STR(argIndex)+"] ="+STR(argListInvoked[argIndex]) 
												erroRoutine(errorMessage)
												return False
											else:
												PRINT ("Replacing",argumentList[argIndex],"with",argInvokedAST )
												argumentInvocationDictionary[argumentList[argIndex]]=argInvokedAST
										PRINT ("argumentInvocationDictionary =",argumentInvocationDictionary )
										PRINT ("=============================================================\n\n\n")
										# Recall the following.
										# - If the macro is variadic and __VA_ARGS__ is null, use null__VA_ARGS__macroExpansionTextAST.
										# - For all other cases, use macroExpansionTextAST.
										if macroIsVariadicWithNull__VA_ARGS__:
											PRINT ("null__VA_ARGS__macroExpansionTextAST =",null__VA_ARGS__macroExpansionTextAST )
											# This is the precise place where we are actually doing the macro expansion
											functionCallResult = replaceArguments (null__VA_ARGS__macroExpansionTextAST, argumentInvocationDictionary)
										else:
											PRINT ("macroExpansionTextAST =",macroExpansionTextAST )
											# This is the precise place where we are actually doing the macro expansion
											functionCallResult = replaceArguments (macroExpansionTextAST, argumentInvocationDictionary)
										if functionCallResult[0] == False:
											PRINT ("Exiting - ERROR while invoking function replaceArguments for macroExpansionTextAST=", macroExpansionTextAST," and argumentInvocationDictionary =",argumentInvocationDictionary )
											return False
										argListInvokedReplaced = functionCallResult[1]
										if '##' in macroExpansionText:
											argListInvokedReplacedDoubleHash = applyDoubleHashOperator(argListInvokedReplaced)
										else:
											argListInvokedReplacedDoubleHash = argListInvokedReplaced
										PRINT ("\n\n\n#### BEGIN ####=============================================================\n\n\n\n")
										PRINT ("macroExpansionText = ",macroExpansionText )
										PRINT ("argumentList = ",argumentList )
										PRINT ("argListInvoked = ",argListInvoked )
										PRINT ("macroExpansionTextAST = ",macroExpansionTextAST )
										PRINT ("argListInvokedReplaced = ", argListInvokedReplaced )
										PRINT ("argListInvokedReplacedDoubleHash = ",argListInvokedReplacedDoubleHash )
										argListInvokedReplacedText = outputTextArithmeticExpressionFromAST(argListInvokedReplacedDoubleHash)
										if argListInvokedReplacedText == False:
											PRINT ("ERROR after calling outputTextArithmeticExpressionFromAST(argListInvokedReplacedDoubleHash) for argListInvokedReplacedDoubleHash =",argListInvokedReplacedDoubleHash )
											return False
										PRINT ("argListInvokedReplacedText =",argListInvokedReplacedText )
										PRINT ("\n\n\n\n#### END ####=============================================================\n\n\n")
										
										# Now replace the text
										macroInvocationSuffix = ""
										macroExpansionPosition = findTokenListInLines(restLines,invocationTokensArgsOnly)
										if macroExpansionPosition == False:
											PRINT ("ERROR after calling findTokenListInLines(restLines,invocationTokensArgsOnly) for restLines =",restLines," and invocationTokensArgsOnly =",invocationTokensArgsOnly )
											return False
										elif macroExpansionPosition[0]<0 or macroExpansionPosition[1]<0 or macroExpansionPosition[2]<0 or macroExpansionPosition[3]<0 or macroExpansionPosition[4]<0:
											PRINT ("ERROR in preProcess() : Was looking for ",invocationTokensArgsOnly, "inside <",restLines )
											PRINT ("macroExpansionPosition = ",macroExpansionPosition )
											return False
											sys.exit()
										else:
											if macroExpansionPosition[4]<len(restLines[macroExpansionPosition[3]])-1:
												macroInvocationSuffix = restLines[macroExpansionPosition[3]][macroExpansionPosition[4]+1:]
												
										# TO-DO: Currently we are putting a space before joining the below 3 fragments so that we accidentally do not concatenate variable names.
										# TO-DO: Try to see if we can do it in a better way (it is currently pretty much a hack).
										newLineAfterMacroInvocation = stringBeforeMacroName + " " + argListInvokedReplacedText + " " + macroInvocationSuffix
										impactedLines = lines[k:k+macroExpansionPosition[3]+1]
										PRINT ("impactedLines = <%s>"%impactedLines )
										PRINT ("newLineAfterMacroInvocation = <%s>"%newLineAfterMacroInvocation )
										PRINT ("\n\n\n\n\nPrinting the existing Lines before macro <",macroName, "> invocation replacement" )
										PRINT ("===============================================" )
										returnStatus = printLines(lines)
										if returnStatus == False:
											return False
										PRINT ("===============================================" )
										lines[k] = newLineAfterMacroInvocation
										delLineIndex = 1
										while delLineIndex <= macroExpansionPosition[3]:
											PRINT ("Removing ALL tokens from lines[",k+delLineIndex,"] =",lines[k+delLineIndex],", essentially making it blank line" )
											lines[k+delLineIndex] = '\n'
											delLineIndex = delLineIndex + 1
										PRINT ("===============================================" )
										PRINT ("\n\n\n\n\nPrinting the existing Lines after macro <",macroName, "> invocation replacement" )
										PRINT ("===============================================" )
										returnStatus = printLines(lines)
										if returnStatus == False:
											return False
										PRINT ("===============================================" )
								
							j=j+1
						
				else:
					PRINT (("currLine = <%s>"%lines[i]) )
					PRINT ("Error in preProcess() in Macro argument-checking code - exiting" )
					return False
					sys.exit()
				
				
			i=i+1

			# After all the lines have been processed, we need to run the comment and macro processing again just in case there are such statements inside the included file
			
			# Remove Multi-line comments
			removeComments()
			
			# Condense each Multi-line Macro into a single-line macro 
			status = condenseMultilineMacroIntoOneLine()
			if status == False:
				errorMessage = "ERROR in preProcess() after calling condenseMultilineMacroIntoOneLine()"
				errorRoutine(errorMessage)
				return False
			
			
#		PRINT ("======================\nAFTER handling multi-line macros\n======================" )
#		PRINT ("len(lines) = ", len(lines) )
		i=0
		while i < len(lines):
			PRINT ((" line # %d = <%s>" % (i,lines[i])) )
			i = i+1


	return True

######################################################################################################################
# This function is supplied with a list of tokens and a list of lines, supposedly matching the tokenlist.
# The coutput is for each token in tokenList, the [<startLineNum,startCharNum>,<endLineNum,endCharNum>]
# TO-DO: What if the same tokenList exists multiple times? It is entirely possible that two macros share some code.
######################################################################################################################
def tokenLocations(lines, tokenList):
	PRINT ("Inside tokenLocations, tokenList =",tokenList )
	tokenizeLinesOutputResult = tokenizeLines(lines)
	if tokenizeLinesOutputResult == False:
		OUTPUT ("Error inside tokenLocations after calling tokenizeLines(lines) for lines =", lines )
		return False
	else:
		tokenizeLinesOutput = tokenizeLinesOutputResult[0]
		
	if tokenList != tokenizeLinesOutput:
		OUTPUT ("ERROR - inside function tokenLocations(), the input tokenList does not correspond to the supplied lines - exiting" )
		OUTPUT ("tokenList = ",tokenList, "lines =", lines )
		return False
		sys.exit()
	else:
		tokenLocationLinesChars = []
		
	
		i = 0
		linePointer = 0
		charPointer = 0
		#TO-DO: Tokens that spread over multiple lines (most likely a quoted literal)
		while i < len(tokenList):
			currentToken = tokenList[i]
			if currentToken != currentToken.strip():
				OUTPUT ("ERROR in tokenLocations() - Illegal currentToken = tokenList[",i,"] =", tokenList[i],"has whitespace at begining or end - exiting" )
				return False
				sys.exit()
			while True:
				if lines[linePointer][charPointer] == currentToken[0]:
					# Check that the string is indeed the token
					if (len(currentToken) <= len(lines[linePointer][charPointer:])) and (currentToken == lines[linePointer][charPointer:charPointer+len(currentToken)]):
						startLineChar = [linePointer,charPointer]
						endLineChar = [linePointer,charPointer+len(currentToken)-1]
						PRINT ("currentToken = tokenList[",i,"] =", tokenList[i],"has location",startLineChar,endLineChar )
						tokenLocationLinesChars.append([startLineChar,endLineChar])
						charPointer = charPointer+len(currentToken)
						if charPointer >= len(lines[linePointer]):
							charPointer = 0
							linePointer = linePointer + 1
						i = i + 1
						break
					else:
						OUTPUT ("ERROR in tokenLocations() - somehow the tokenstream does not correspond to the lines - exiting" )
						OUTPUT ("currentToken = tokenList[",i,"] =", tokenList[i]," linePointer =", linePointer, "charPointer =",charPointer, "lines[linePointer][charPointer]=",lines[linePointer][charPointer] )
						return False
						
				elif lines[linePointer][charPointer].isspace():	# TO-DO: what if this catches the newline
					charPointer = charPointer + 1
					if charPointer >= len(lines[linePointer]):
						charPointer = 0
						linePointer = linePointer + 1
				elif lines[linePointer][charPointer]=='\n':	# TO-DO: what if this catches the newline
					PRINT ("ALERT: Newline" )
					charPointer = charPointer + 1
					if charPointer >= len(lines[linePointer]):
						charPointer = 0
						linePointer = linePointer + 1
					else:
						OUTPUT ("ERROR in tokenLocations() - should never come here - exiting!" )
						return False

				else:
					OUTPUT ("ERROR in tokenLocations() - Illegal character - exiting" )
					OUTPUT ("currentToken = tokenList[",i,"] =", tokenList[i]," linePointer =", linePointer, "charPointer =",charPointer, "lines[linePointer][charPointer]=",lines[linePointer][charPointer] )
					return False
					
		return tokenLocationLinesChars


################################################################################################################################
# This function takes in a tokenList where a enum definition or declaration is happening from token # i 
################################################################################################################################
def parseEnum(tokenList, i):
	global typedefs, enums, lines, structuresAndUnionsDictionary, primitiveDatatypeLength, variableDeclarations, totalVariableCount
	
	if not isinstance(tokenList,list):
		errorMessage = "ERROR in parseEnum(): tokenList <"+STR(tokenList)+"> is not a list"
		errorRoutine(errorMessage)
		return False
	elif not tokenList:
		errorMessage = "ERROR in parseEnum(): Empty passed tokenList"
		errorRoutine(errorMessage)
		return False
	elif (not isinstance(i,int)) or i <0 or i>=len(tokenList):
		errorMessage = "ERROR in parseEnum(): Illegal value of i ="+STR(i)
		errorRoutine(errorMessage)
		return False
	else:
		
		# Sanity check: Ensure that enums and enumFieldValues are in sync
		if (not enums) and (not enumFieldValues):
			PRINT ("enums and enumFieldValues are both empty, hence in sync" )
		elif (enums and not enumFieldValues) or (not enums and enumFieldValues):
			PRINT ("ERROR in parseEnum(): enums and enumFieldValues are out of sync - one of them is empty while the other is not" )
			PRINT ("enums =", enums )
			PRINT ("enumFieldValues =",enumFieldValues )
			return False
		elif enums and enumFieldValues:
			tempEnumFieldValues = {}
			for key in enums.keys():
				for field in enums[key]:
					if field in getDictKeyList(tempEnumFieldValues):
						PRINT ("ERROR: Duplicate enum field", field )
						return False
					elif field not in getDictKeyList(enumFieldValues):
						PRINT ("ERROR: enum field", field, "NOT found in enumFieldValues" )
						return False
					else:
						tempEnumFieldValues[field]=enums[key][field]
			if len(tempEnumFieldValues) != len(enumFieldValues):
				PRINT ("len(tempEnumFieldValues) = ",len(tempEnumFieldValues), "!=", "len(enumFieldValues) =", len(enumFieldValues) )
				PRINT ("Which possibly means that enumFieldValues has more entries" )
				PRINT ("enums =",enums, "tempEnumFieldValues = ",tempEnumFieldValues, "enumFieldValues =", enumFieldValues )
				
		else:
			PRINT ("ERROR: The control should have never come here (ensuring that enums and enumFieldValues are in sync)" )
			sys.exit()
			return False
	
		nextSemicolonIndex = i+1 + tokenList[i+1:].index(";")
		enumStatementStartIndex = i
		if nextSemicolonIndex <= i + 2:
			errorMessage = "ERROR in parseEnum() - Illegal statement formation (semicolon without adequate enum variable type and name) - exiting"
			errorRoutine(errorMessage)
			PRINT ("ERROR in parseEnum() processing ENUM - nextSemicolonIndex =",nextSemicolonIndex,"tokenList[i:] = tokenList[",i,":]=",tokenList[i:] )
			return False
		else:
		
			# There are four cases possible.
			
			# 1. enum Declaration YES, Definition NO	- enum WEEKDAY day1,day2;
			# 2. enum Declaration NO , (named) Definition NO   - enum {Mon, Tue};			- Anonymous
			# 3. enum Declaration YES, Definition YES   - enum WEEKDAY {Mon, Tue} day1,day2;
			# 4. enum Declaration NO , Definition YES	- enum {Mon, Tue} day1, day2;
		
		
			# Step 1. we handle the enumDataType. There are three cases possible: 1) Previously-defined, 2) Anonymous, and 3) Now-defined
		
		
			# 1. Declaration of previously-defined enums, NO defintion. So, need to check if the enum really exists or not.
			if tokenList[i+1] != "{" and tokenList[i+2] != "{" :
				enumDataType = tokenList[i+1]
				if enumDataType not in getDictKeyList(enums):
					errorMessage = "ERROR - enum name <%s> does NOT exist - exiting"%enumDataType
					errorRoutine(errorMessage)
					PRINT ("ERROR in parseEnum() processing ENUM declaration - nextSemicolonIndex =",nextSemicolonIndex,"tokenList[i:nextSemicolonIndex] = tokenList[",i,":",nextSemicolonIndex,"]=",tokenList[i:nextSemicolonIndex] )
					return False
			
			# 2. Anonymous enum datatype definition
			elif tokenList[i+1] == "{":
				PRINT ("WARNING: Anonymous enum declaration!!" )
				curlyBraceStartIndex = i + 1
				totalNumberOfAnonymousEnumsTillNow = 0
				anonymousEnumPrefix = "AnonymousEnum+"		# We cannot have the plus sign as part of any enum datatype  name
				if enums:
					for key in enums.keys():
						if key.startswith(anonymousEnumPrefix):
							num = int(key[len(anonymousEnumPrefix):])
							if num > totalNumberOfAnonymousEnumsTillNow:
								totalNumberOfAnonymousEnumsTillNow = num
				enumDataType = anonymousEnumPrefix+str(totalNumberOfAnonymousEnumsTillNow+1)

			# 3. New enum datatype definition
			elif tokenList[i+2] == "{":
				enumDataType = tokenList[i+1]
				# Check if the enum already exists or not - do this ONLY if we are defining the enum here. 
				# Without the definition, there can be many declarations beginning with the same enum type.
				if enumDataType in getDictKeyList(enums):
					errorMessage = "ERROR - enum name <%s> already exists - exiting"%enumDataType
					errorRoutine(errorMessage)
					PRINT ("ERROR in parseEnum() processing ENUM - nextSemicolonIndex =",nextSemicolonIndex,"tokenList[i:nextSemicolonIndex] = tokenList[",i,":",nextSemicolonIndex,"]=",tokenList[i:nextSemicolonIndex] )
					return False
				else:
					PRINT ("New enum datatype",enumDataType, "will be added" )

			#########################################################################################
			# Step 2. We handle the enum definition. Basically if the { ... } exists, we deal with it.
			# Previously, we have covered the three cases where the enumDataType is 1) previously defined, 2) Anonymous, and 3) Newly defined.
			# The reason we are doing this is because we want to carve out the Enum definition part (anonymous or not) into a single block.
			
			if (tokenList[i+1]=='{' or tokenList[i+2] == '{'): # Definition, not declaration
				curlyBraceStartIndex = i+1+tokenList[i+1:nextSemicolonIndex].index('{')
				
				# The assumption here is a that there cannot be any curly braces inside the enum expression
				if '}' not in tokenList[i+2:nextSemicolonIndex]:
					errorMessage = "ERROR - in parseEnum() processing ENUM - NO cruly brace end before semicolon!"
					errorRoutine(errorMessage)
					PRINT ("ERROR in parseEnum() processing ENUM - nextSemicolonIndex =",nextSemicolonIndex,"tokenList[i:nextSemicolonIndex] = tokenList[",i,":",nextSemicolonIndex,"]=",tokenList[i:nextSemicolonIndex] )
					return False
					# Enum definition
					
				else:		
					curlyBraceEndIndex = i+1+tokenList[i+1:nextSemicolonIndex].index('}')
					PRINT ("Going to create new enum variable named",enumDataType )
					enumExpression = tokenList[curlyBraceStartIndex:curlyBraceEndIndex+1]	# Both the braces need to be included in the expression
					parseArgumentListResult = parseArgumentList(enumExpression)
					
					if parseArgumentListResult == False:
						errorMessage = "ERROR - in parseEnum() processing ENUM - the enumExpression =<%s> cannot be parsed properly"%enumExpression
						errorRoutine(errorMessage)
						PRINT ("ERROR in parseEnum() processing ENUM - nextSemicolonIndex =",nextSemicolonIndex,"tokenList[i:nextSemicolonIndex] = tokenList[",i,":",nextSemicolonIndex,"]=",tokenList[i:nextSemicolonIndex] )
						return False
					else:
						PRINT ("After parsing the enumExpression =",enumExpression,"parseArgumentListResult =",parseArgumentListResult )
						# This variable indicates the last ENUM-ed value. We put it deliberately at -1 so that we do not need to have some special logic for the first element.
						lastEnumValue = -1
						enumFields = {} # This is a dictionary that will hold the various ENUMed values
						for enumElement in parseArgumentListResult:
							PRINT ("Handling ENUM element", enumElement, "of length",len(enumElement) )
							# When there is explicit assignment to a enum element, we know for sure that the enumElement is returned as a list.
							# However, when it is just the element itself without any explicit assignment, we do not know if enumElement is a single-element list, or a string.
							# If enumElement is returned as a string, len(enumElement) will NOT show as 1, but rather the number of characters in the string (1 or more).
							# Hence, we do explicit assignment of the element name (called "item" here) and the length of the enumElement
							if isinstance(enumElement,list):
								# GCC allows even formations like this: enum {A, B,}. In that case, the parseArgumentListResult will return 3 elements - A, B, and a blank list
								if not enumElement:
									continue
								item = enumElement[0]
								enumElementLength = len(enumElement)
							else:
								item = enumElement
								enumElementLength = 1
							PRINT ("Going to check if the enum element",item,"already appears as some other enum constant anywhere else" )
							# This is the list of ALL possible ENUMed field names
							allEnumedValues = []
							allEnumedValuesStr = ""
							for definedEnumtype in enums.keys():
								allEnumedValuesStr += "\n<"+definedEnumtype+"> "
								for definedEnumtypeValues in enums[definedEnumtype].keys():
									allEnumedValues.append(definedEnumtypeValues)
									allEnumedValuesStr += definedEnumtypeValues + " "
							PRINT ("allEnumedValues =",allEnumedValues )
							PRINT ("The above list should be the same as the one below with the <enum type> extra" )
							PRINT (allEnumedValuesStr )
							
							if item in cDataTypes or item in cKeywords or item in getDictKeyList(typedefs) or item in getDictKeyList(structuresAndUnionsDictionary) or item in getDictKeyList(enums) or item in allEnumedValues:
								errorMessage = "ERROR parseEnum() processing ENUM - illegal enum element <%s>"%item
								errorRoutine(errorMessage)
								return False
							elif enumElementLength == 1:	# Be careful not to use enumElement[0], since we do not know if the enumElement is a single-element list, or a string
								enumFields[item]= lastEnumValue+1
								lastEnumValue += 1
								PRINT ("No explicit assignment for",item )
							elif enumElement[1] != "=":
								errorMessage = "ERROR parseEnum() - illegal enum element <%s> - should have been =  .... Exiting"%enumElement[1]
								errorRoutine(errorMessage)
								return False
							elif enumElementLength == 3:
								PRINT ("Simple assignment - no expression to evaluate for enum field", item )
								if isinstance(enumElement[2],int):	# Will it work? "1" is not an integer, 1 is
									enumFields[enumElement[0]]= enumElement[2]
									lastEnumValue += 1
								elif checkIfString(enumElement[2]):	# Will it work? "1" is not an integer, 1 is
									enumFields[enumElement[0]]= evaluateArithmeticExpression(enumElement[2])
									lastEnumValue += 1
								else:
									errorMessage = "ERROR parseEnum() - illegal enum element assignment <%s> = <%s> (not an integer) - should have been =  .... Exiting"%(enumElement[0],enumElement[2])
									errorRoutine(errorMessage)
									return False
							else:
								PRINT ("Complex assignment - need to evaluate the expression for enum field", item )
								arithmeticExpression = enumElement[2:]
								PRINT ("Going to evaluate the expression",enumElement[0],"=",arithmeticExpression )
								parseArithmeticExpressionOutput = parseArithmeticExpression(arithmeticExpression)
								if parseArithmeticExpressionOutput == False:
									errorMessage = "ERROR parseEnum() after calling parseArithmeticExpression()"
									errorRoutine(errorMessage)
									return False
								else:
									evaluateArithmeticExpressionOutput = evaluateArithmeticExpression(parseArithmeticExpressionOutput)
									if evaluateArithmeticExpressionOutput[0] != True:
										errorMessage = "ERROR parseEnum() after calling evaluateArithmeticExpression()"
										errorRoutine(errorMessage)
										return False
									else:
										output = evaluateArithmeticExpressionOutput[1]
										if isinstance(output,int):
											enumFields[enumElement[0]] = output
											lastEnumValue = output
											PRINT ("output =",output,"is indeed an assignable integer." )
										else:
											errorMessage = "ERROR parseEnum() after calling evaluateArithmeticExpression() - the output ("+str(output)+") is not an integer"
											errorRoutine(errorMessage)
											return False
											
						PRINT ("Current content of the enums dictionary:" )
						PRINT (enums )
						PRINT ("Current content of the ALL possible enums values:" )
						PRINT (enumFieldValues )
						PRINT ("Going to add the following dictionary for enumDataType =", enumDataType, " :" )
						PRINT (enumFields )
						
						enums[enumDataType]=enumFields
						for field in enumFields.keys():
							if field in getDictKeyList(enumFieldValues):
								PRINT ("ERROR: enum field",field,"already defined" )
								return False
							else:
								enumFieldValues[field] = enumFields[field]
						
			###################################################################################################
			# Step 3. Now we handle the declarations
			
			if '}' in tokenList[enumStatementStartIndex:nextSemicolonIndex]: 	# The definition precedes the declarations, if any
				if curlyBraceEndIndex + 1 == nextSemicolonIndex:
					PRINT ("No enum variables to instantiate for",enumDataType, "we are done here" )
					i = nextSemicolonIndex+1
					return i
				else:
					declarationStartIndex = curlyBraceEndIndex + 1
					# When we have both enum defintion and declaration in the same statement, break it up. 
					# Create a fake entry, as if the enum definition was done first
					if enumStatementStartIndex>0 and tokenList[enumStatementStartIndex-1] == "typedef":
						memberDeclarationStatement = ["typedef","enum", enumDataType]
						numFakeEntries = 3
					else:
						memberDeclarationStatement = ["enum", enumDataType]
						numFakeEntries = 2
					memberDeclarationStatement.extend(tokenList[curlyBraceEndIndex+1:nextSemicolonIndex+1])
			else:	# No defintion, just declarations
				memberDeclarationStatement = tokenList[enumStatementStartIndex:nextSemicolonIndex+1]
				declarationStartIndex = enumStatementStartIndex + 2
				
			PRINT ("Going to parse memberDeclarationStatement =",memberDeclarationStatement )
			parsed5tupleList = parseVariableDeclaration(memberDeclarationStatement)
			if parsed5tupleList == False:
				PRINT ("ERROR in parseEnum() enum declaration after calling parseVariableDeclaration(memberDeclarationStatement) for memberDeclarationStatement =",memberDeclarationStatement )
				return False
			else:
				PRINT ("enum variables declaration",parsed5tupleList, "parsed" )
				for item in parsed5tupleList:
					PRINT ("enum ",enumDataType,"has the following declarations after it" )
					PRINT ("Main enum variable name is ",item[0],"of size",item[1],"and it is located at relative index of ",item[3],"inside the variable declaration statement",item[2] )
					# Each member of the list follows exactly the same format as the parsed5tupleList, with one key addition - the 6th item.
					# This 6th member now represents the absolute index (within the tokenList) of the variable name.
					if tokenList[declarationStartIndex+item[3]-numFakeEntries]!=item[0]:
						PRINT ("ERROR in parseEnum() enum - for declarationStartIndex =",declarationStartIndex,"tokenList[declarationStartIndex+item[3]-numFakeEntries] = tokenList[",declarationStartIndex,"+",item[3],"-",numFakeEntries,"]",tokenList[declarationStartIndex+item[3]-numFakeEntries],"!=item[0]=",item[0] )
						return False
						sys.exit()
					else:
						globalTokenListIndex = declarationStartIndex+item[3]-numFakeEntries
						
						variableDescriptionExtended = item[4]
						variableDescriptionExtended["globalTokenListIndex"]=globalTokenListIndex
						variableDescriptionExtended["parentVariableType"]=["enum",enumDataType]
#						variableDescriptionExtended["parentVariableName"]=enumDataType
						variableDescriptionExtended["variableId"] = totalVariableCount
						totalVariableCount += 1
						variableDeclarations.append([item[0],item[1],item[2],item[3],variableDescriptionExtended]) 
		
			
			i = nextSemicolonIndex + 1
		
		return i					

def declarationHasBitfields(tokenList):
	if checkIfString(tokenList):
		return False
	elif not isinstance(tokenList,list):
		errorMessage = "ERROR in declarationHasBitfields: tokenList <"+STR(tokenList)+"> is not a list"
		errorRoutine(errorMessage)
		return False
		
	countQuestionMarks = 0
	countColons = 0
	
	for item in tokenList:
		if item == ';':
			break
		elif item == '?':
			countQuestionMarks += 1
		elif item == ':':
			countColons += 1
		else:
			pass
	
	if countQuestionMarks == countColons:
		return False
	elif countQuestionMarks == countColons - 1:
		return True
	else:
		errorMessage = "ERROR in declarationHasBitfields: tokenList <"+STR(tokenList)+"> has "+countQuestionMarks+" number of ? but "+countColons+" number of : before hitting the ;"
		errorRoutine(errorMessage)
		return False
		


#######################################################################################################################
# This function takes in a tokenList and an index pointing to the start of the derived type declaration and parses it	
# What it essentially does is that if there is any Derived type (basically typedef) in the declaration statement, 
# it converts that statement into one that will only contain the primitive types (int, float, char etc.).
#######################################################################################################################
def convertDerivedTypeDeclarationIntoBaseTypeDeclaration(tokenList, i):

	nextSemicolonIndex = i+1 + tokenList[i+1:].index(";")
	
	PRINT ("\n\n","=="*50,"\n","Inside convertDerivedTypeDeclarationIntoBaseTypeDeclaration(), going to evaluate", tokenList[i:nextSemicolonIndex+1])
	
	# The way we resolve the case when a base storage is a derived kind. We find out what was the original typedef's declaration statement, and 
	# then we plug in the current variable declaration in that statement.
	#
	# For example, if we have the following:
	#
	#  		typedef int INT[2]; 
	#  		INT * i[3];
	#
	# We plug in the second statement into the first after parenthesizing it. Basically, in the first declaration, replace INT with (* i[3]) and remove the typedef.
	#
	#		int (* i[3])[2];
	#
	# The problem happens when we have multiple declarations, both for typedefs declarations, and variable declarations. Like below:
	#
	#  		typedef int *ptrINT, INT[2]; 		==> we have to break it down to individual "isolated" declarations, like <int *ptrINT> and <int INT[2]>
	#  		ptrINT * i[3], (*func[2])(int);		==> we have to break it down to individual "isolated" declarations, like <* i[3]> and <(*func[2])(int)>
	#
	# Only after we break it down to individual pieces, we can do the plugging in. We do this splitting by calling parseArgumentList().
	# This function was originally written for parsing function arguments, so it expects the input list to be parenthesized. Hence we parenthesize it artificially.
	#
	# The only problem is that when I parenthesize things, it does not work for bitfields. For example, if we have this code originally:
	#
	#  		typedef unsigned long long uint64_t;
	#  		uint64_t    var :3;
	#
	# When we transform (or plug in back) the second expression in the first one, we get this:
	#
	# 		unsigned long long (var :3);
	#
	# The compiler like GCC will not accept this. So, we are taking a risk here. We are going to take the following strategy:
	# If it involves bitfield, we are going to straight plug it back in WITHOUT the parenthesis. This should not give us a lot of problems, because
	# usually bitfields do not support arrays, and you cannot have standalone bitfield variable declarations - bitfields are only allowed witin structs.
	# It is possible to have regular non-bitfield variable declaration and bitfield declaration in the same statement, like this:
	#
	#  		uint64_t a, b:3, c;
	#
	# But we are still hoping that it will simple typedefs, in which case we will be fine. If it has complex typedefs, there might be a problem.

	# Basically we are trying to figure out what all tokens occur before the derived type
	statementStartIndex = i
	while statementStartIndex > 0 and tokenList[statementStartIndex-1] in ('auto','register','static','extern', 'const','volatile', 'typedef'):
		statementStartIndex -= 1

	derivedTypeIndex = i
	while tokenList[derivedTypeIndex] in ('auto','register','static','extern', 'const','volatile'):
		derivedTypeIndex += 1

	fragmentBeforeDerivedType = tokenList[statementStartIndex:derivedTypeIndex]
	PRINT("fragmentBeforeDerivedType =",fragmentBeforeDerivedType)
	
	if tokenList[derivedTypeIndex] not in getDictKeyList(typedefs):
		errorMessage = "Supplied tokenList[derivedTypeIndex=",derivedTypeIndex,"] =",tokenList[derivedTypeIndex],"is not a declared type"
		errorRoutine(errorMessage)
		return False
		
	PRINT ("Found a previously defined type",tokenList[derivedTypeIndex],", whose details are",typedefs[tokenList[derivedTypeIndex]] )
	previouslyCreatedType = tokenList[derivedTypeIndex]
	originalTypedefCreationStatement = typedefs[previouslyCreatedType][2]
	typedefVariableIndex = typedefs[previouslyCreatedType][3]
	originalTypedefCreationStatementTypeSpecifierEndIndex = typedefs[previouslyCreatedType][4]["typeSpecifierEndIndex"]
	
	originalTypedefDeclarationSegmentStartIndex = typedefs[previouslyCreatedType][4]["currentDeclarationSegmentStartIndex"]
	originalTypedefDeclarationSegmentEndIndexInclusive = typedefs[previouslyCreatedType][4]["currentDeclarationSegmentEndIndexInclusive"]
	originalTypedefCreationStatementDeclarationSegmentIsolated = originalTypedefCreationStatement[originalTypedefDeclarationSegmentStartIndex:originalTypedefDeclarationSegmentEndIndexInclusive]
	
	
	PRINT ("For created type <",previouslyCreatedType,">, the originalTypedefCreationStatement =",originalTypedefCreationStatement )
	if "typedef" not in originalTypedefCreationStatement[:originalTypedefCreationStatementTypeSpecifierEndIndex]:
		errorMessage = "ERROR in convertDerivedTypeDeclarationIntoBaseTypeDeclaration() - the variable declaration statement for"+STR(previouslyCreatedType)+" doesn't have the string \"typedef\""
		errorRoutine(errorMessage)
		return False
	elif typedefs[previouslyCreatedType][0] != previouslyCreatedType:
		errorMessage = "ERROR in convertDerivedTypeDeclarationIntoBaseTypeDeclaration() - the variable declaration statement for "+STR(previouslyCreatedType)+" declare some other variable "+STR(typedefs[previouslyCreatedType][0])
		errorRoutine(errorMessage)
		return False
	
	# The original typedef statement might contain multiple different types created within a single typedef statement.
	# So, we need to break it up and find out which one has it
	temp = ["("]+originalTypedefCreationStatement[originalTypedefCreationStatementTypeSpecifierEndIndex+1:-1]+[")"]
	PRINT ("Going to parse the possibly multiple typedef creations in a single typedef statement = <%s>"%temp )
#	parseArgumentListResult = parseArgumentList(temp, omitColons=False)	# This is causing the statement to fail when we had both bitfield and typedef in the same declaration.
	parseArgumentListResult = parseArgumentList(temp, omitColons=True)
	if parseArgumentListResult == False:
		errorMessage = "ERROR in convertDerivedTypeDeclarationIntoBaseTypeDeclaration() while breaking up the original typedef creation statement by calling parseArgumentList(%s)"%(STR(temp))
		errorRoutine(errorMessage)
		return False
	
	PRINT ("For splitting the original typedef creation statement <%s>, parseArgumentListResult ="%(STR(originalTypedefCreationStatement)) )
	for item in parseArgumentListResult:
		PRINT (item )
	# We want to find out which typedef creation fragment contains our sought type 
	indexConsumedTillNow = originalTypedefCreationStatementTypeSpecifierEndIndex
	foundTheCorrectFragment = False
	for itemIndex in range(len(parseArgumentListResult)):
		currentItem = parseArgumentListResult[itemIndex]
		if checkIfString(currentItem):
			currentItem = [currentItem]
		elif not isinstance(currentItem,list):
			errorMessage = "ERROR: In convertDerivedTypeDeclarationIntoBaseTypeDeclaration(), Somehow the currentItem = <"+STR(currentItem)+"> is neither list nor string"
			errorRoutine(errorMessage)
			return False
		
		PRINT ("Created type # ",itemIndex, " = ", currentItem, "(the fragment)" )
		if indexConsumedTillNow+1 <= typedefVariableIndex <= indexConsumedTillNow+len(currentItem):
			PRINT ("Found the index",typedefVariableIndex )
			
			# We will later just use this, currently just using it to verify that both results are the same
#						if originalTypedefCreationStatementDeclarationSegmentIsolated != parseArgumentListResult[itemIndex]:
#							errorMessage = "ERROR: originalTypedefCreationStatementDeclarationSegmentIsolated = <"+STR(originalTypedefCreationStatementDeclarationSegmentIsolated)+"> does not match with parseArgumentListResult[itemIndex="+STR(itemIndex)+"] = <"+STR(parseArgumentListResult[itemIndex])+">"
#							errorRoutine(errorMessage)
#							return False
			
			originalTypedefCreationStatementIsolated = originalTypedefCreationStatement[:originalTypedefCreationStatementTypeSpecifierEndIndex+1]+currentItem+[";"]
			# Since we are artificially creating a new construct containing a single type creation, we also need to adjust at what index we will find the new type
			typedefVariableIndexIsolated = originalTypedefCreationStatementTypeSpecifierEndIndex + typedefVariableIndex - indexConsumedTillNow
			if originalTypedefCreationStatementIsolated[typedefVariableIndexIsolated] != previouslyCreatedType:
				errorMessage = "ERROR in convertDerivedTypeDeclarationIntoBaseTypeDeclaration(): the isolated typedef creation statement (%s) does not have %s at its index # %d"%(STR(originalTypedefCreationStatementIsolated,previouslyCreatedType,typedefVariableIndexIsolated))
				errorRoutine(errorMessage)
				return False
			else:
				PRINT ("For originalTypedefCreationStatementIsolated=<%s> and typedefVariableIndexIsolated=%d, originalTypedefCreationStatementIsolated[typedefVariableIndexIsolated]=%s"%(originalTypedefCreationStatementIsolated,typedefVariableIndexIsolated,originalTypedefCreationStatementIsolated[typedefVariableIndexIsolated]) )
				foundTheCorrectFragment = True
				break
		else:
			PRINT ("Did not find index #",typedefVariableIndex,"within index range <",indexConsumedTillNow+1,",",indexConsumedTillNow+len(currentItem)+1,"> (both indices inclusive)" )
			indexConsumedTillNow += len(currentItem) + 1 # The extra 1 at the end is for the comma (remember, multiple typedef declarations)
			PRINT ("Upping the indexConsumedTillNow to",indexConsumedTillNow )
			
	if foundTheCorrectFragment == False:
		errorMessage = "ERROR in convertDerivedTypeDeclarationIntoBaseTypeDeclaration(): Somehow did not find the %s within the typedef creation statement (%s)"%(previouslyCreatedType,STR(originalTypedefCreationStatement))
		errorRoutine(errorMessage)
		return False
		

	# We have located which part of the original typedef creation statement we need to plug in our new variable declaration into. 
	# However, remember that even the existing declarations can also have multiple variable declarations. So, we need to split it first.
	# For that, we deliberately parenthesize it because the parseArgumentList() expects the input to be structured that way.
	
	possiblyMultipleVariableDeclarations = ["("] + tokenList[i+1:nextSemicolonIndex]+ [")"]
	# We can have multiple variables declared under this same variable declared statement (separated by comma). So, we separate them.
#	parseArgumentListResult = parseArgumentList(possiblyMultipleVariableDeclarations)	# This was creating problems with bitfields
	parseArgumentListResult = parseArgumentList(possiblyMultipleVariableDeclarations, omitColons = True)
	if parseArgumentListResult == False:
		errorMessage = "ERROR in convertDerivedTypeDeclarationIntoBaseTypeDeclaration() while breaking up the variable declaration statement <%s> by calling parseArgumentList() where the base storage is a created type"%(STR(possiblyMultipleVariableDeclarations))
		errorRoutine(errorMessage)
		return False
	else:
		PRINT ("For splitting the created type variable declaration statement, parseArgumentListResult =" )
		for item in parseArgumentListResult:
			PRINT (item )
		
		# We just want to scoop up the portion of the original typedef statement that we can re-use again and again for each of the current var declarations.
		# This means we are omiting the semicolon at the end
		
		convertedMultipleDeclarations = []
		# If the current statement, which uses a created type as base storage, is yet another typedef, then we need to put an extra typedef at the beginning.
#		if i>0 and tokenList[i-1]=="typedef":
#			convertedMultipleDeclarations.append("typedef")
		convertedMultipleDeclarations = fragmentBeforeDerivedType
		
		# Remember that the original typedef creation statement, the string "typedef" may or may NOT be the first item. C allows it to be anywhere.
		# So, we remove the "typedef" from the original string.
		originalBaseStorageSpecifierStatementAfterTypedefRemoval = originalTypedefCreationStatementIsolated[:originalTypedefCreationStatementTypeSpecifierEndIndex+1]
		originalBaseStorageSpecifierStatementAfterTypedefRemoval.remove("typedef")
		PRINT ("Removed the string \"typedef\" from originalTypedefCreationStatementIsolated[:originalTypedefCreationStatementTypeSpecifierEndIndex+1] = <",originalTypedefCreationStatementIsolated[:originalTypedefCreationStatementTypeSpecifierEndIndex+1],">" )
		PRINT ("And added the \"typedef\"-removed string <",originalBaseStorageSpecifierStatementAfterTypedefRemoval,"> to the convertedMultipleDeclarations" )
		convertedMultipleDeclarations.extend(originalBaseStorageSpecifierStatementAfterTypedefRemoval)
		PRINT ("So that now the base storage specifier for convertedMultipleDeclarations = ",convertedMultipleDeclarations )
		
		for listIndex in range(len(parseArgumentListResult)):
			item = parseArgumentListResult[listIndex]	# TO-DO: Looks like when it returns a single-item, it returns it as string (as opposed to a list with a single string item)
		
			replacedTypedefCreationStatement = originalTypedefCreationStatementIsolated[originalTypedefCreationStatementTypeSpecifierEndIndex+1:typedefVariableIndexIsolated]
			
			typedefReplacement = []
			
			# We deliberately put the braces around the item, or else it will not work. It's a MUST
			
			# If it is a bitfield, do not put the additional parenthesis markers at the beginning or the end.
			doNotParenthesize = declarationHasBitfields(item)
			
			if not doNotParenthesize:
				typedefReplacement.append("(")
			if isinstance(item,list):
				typedefReplacement.extend(item)
			elif checkIfString(item):
				typedefReplacement.append(item)
			else:
				errorMessage = "ERROR in convertDerivedTypeDeclarationIntoBaseTypeDeclaration() - the output <%s> from parseArgumentList() is neither list nor string"%(STR(item))
				errorRoutine(errorMessage)
				return False
			if not doNotParenthesize:
				typedefReplacement.append(")")
			
			PRINT ("We are going to replace the <",previouslyCreatedType,"> in the original typedef creation statement with <",typedefReplacement,">" )
			replacedTypedefCreationStatement.extend(typedefReplacement)
			
			replacedTypedefCreationStatement.extend(originalTypedefCreationStatementIsolated[typedefVariableIndexIsolated+1:-1])
			
			if replacedTypedefCreationStatement[-1] == ";":
				errorMessage = "CODING ERROR: Somehow picked up the semicolon at the end - exiting"
				errorRoutine(errorMessage)
				sys.exit()

			if listIndex == len(parseArgumentListResult)-1:
				replacedTypedefCreationStatement.append(";")
			else:
				replacedTypedefCreationStatement.append(",")
				
			convertedMultipleDeclarations.extend(replacedTypedefCreationStatement)
			
			PRINT ("So individual originalTypedefCreationStatementIsolated = <",originalTypedefCreationStatementIsolated,"> now became <",convertedMultipleDeclarations,">" )
			
		list2parse = convertedMultipleDeclarations
		PRINT ("Returning the following from convertDerivedTypeDeclarationIntoBaseTypeDeclaration()\n\n", list2parse,"\n\n","=="*50,"\n")
		
		return list2parse


##############################################################################################################################################
##############################################################################################################################################
##																																			##
## 		This function takes in a tokenList where a structure definition (starting with '{', ending with '}') is happening from token # i 	##
##		The return value is the name of the structure, which is global. This is particularly useful for Anynymous structure.				##
##		The third parameter is parentStruct. It is mostly used for Nested structure. For top-level structs, this value is "--Global--" 		##
##      The reason we choose "--Global--" is because it is NOT a valid identifier name. So it cannot clash.									##
##		The fourth parameter is the level. It tells at what scope level this structure is.													##
##																																			##
##		This is the function that adds the entry to the structuresAndUnionsDictionary{}. It does not do anything to the typedefs{}      	##
##																																			##
##############################################################################################################################################
##############################################################################################################################################

def parseStructure(tokenList, i, parentStructName, level):
	PRINT ("="*30,"\nInside parseStructure()\n","="*30,"\n" )
	global typedefs, enums, lines, structuresAndUnionsDictionary, primitiveDatatypeLength, variableDeclarations, dummyVariableCount, totalVariableCount

	curlyBraceStartIndex = i

	######################################################
	# Check for all possible immediately-catchable errors
	if not isinstance(tokenList,list):
		errorMessage = "ERROR in parseStructure(): tokenList <"+STR(tokenList)+"> is not a list"
		errorRoutine(errorMessage)
		return False
	elif not tokenList:
		errorMessage = "ERROR in parseStructure(): Empty passed tokenList"
		errorRoutine(errorMessage)
		return False
	elif (not isinstance(i,int)) or i <0 or i>=len(tokenList):
		errorMessage = "ERROR in parseStructure(): Illegal value of i ="+STR(i)
		errorRoutine(errorMessage)
		return False
	elif tokenList[i] != '{' :
		errorMessage = "ERROR in parseStructure(): tokenList[i] =  tokenList[" + STR(i) + "] = <" + STR(tokenList[i]) + "> is not a struct or union"
		errorRoutine(errorMessage)
		return False

	# Find out from where the struct definition statement actually starts
	structDefinitionStartIndex = i
	structOrUnionTypeIndex = -100000000	# By default error value
	while True:
		if tokenList[structDefinitionStartIndex] in ("struct","union"):
			structOrUnionTypeIndex = structDefinitionStartIndex
		if structDefinitionStartIndex == 0:
			break
		elif tokenList[structDefinitionStartIndex-1] in (';','{'):	# we could very well have cascaded struct definition, hence checking for the '{' is important
			break
		structDefinitionStartIndex -= 1
	
	if structOrUnionTypeIndex < 0:
		errorMessage = "ERROR in parseStructure(): No struct or union definition statement found"
		errorRoutine(errorMessage)
		return False
	else:
		PRINT("tokenList[structOrUnionTypeIndex =",structOrUnionTypeIndex,"] =",tokenList[structOrUnionTypeIndex])
		structOrUnionType = "struct" if tokenList[structOrUnionTypeIndex] == "struct" else  "union" if tokenList[structOrUnionTypeIndex] == "union" else "ERROR"
		if structOrUnionType not in ("struct","union"): 
			OUTPUT("Coding bug in parseStructure() - exiting")
			sys.exit()

	PRINT("The", tokenList[structOrUnionTypeIndex] ,"definition starts from token[",structDefinitionStartIndex,"] = ",tokenList[structDefinitionStartIndex])

	if ("struct" in tokenList[structDefinitionStartIndex:i]) and ("union" in tokenList[structDefinitionStartIndex:i]):
		errorMessage = "ERROR in parseStructure(): Cannot say that it is both struct and union. tokenList[structDefinitionStartIndex(%d):i(%d)] = %s"%(structDefinitionStartIndex,i,STR(tokenList[structDefinitionStartIndex:i]))
		errorRoutine(errorMessage)
		return False
	elif "}" not in tokenList[curlyBraceStartIndex:]:
		PRINT ("ERROR in parseStructure() - no matching { for struct declaration for ", structName, " - exiting" )
		errorMessage = "ERROR in parseStructure() - no matching { for struct declaration for %s - exiting"%(structName)
		errorRoutine(errorMessage)
		return False
	elif matchingBraceDistance(tokenList[curlyBraceStartIndex:]) < 1:
		PRINT ("ERROR in parseStructure() - cannot find matching brace in",tokenList[curlyBraceStartIndex:], " - exiting!" )
		errorMessage = "ERROR in parsing - cannot find matching brace in tokenlist starting from token %s "% (tokenList[curlyBraceStartIndex])
		errorRoutine(errorMessage)
		return False
	elif not checkIfString(parentStructName):
		PRINT ("parentStructName =",parentStructName)
		errorMessage = "ERROR in parseStructure(): parentStructName = <"+STR(parentStructName)+"> is not a a valid string"
		errorRoutine(errorMessage)
		return False
	elif parentStructName != "--Global--" and parentStructName not in getDictKeyList(structuresAndUnionsDictionary):
		errorMessage = "ERROR in parseStructure() - parentStructName = <"+parentStructName+"> is not a valid parent struct/union - exiting!" 
		errorRoutine(errorMessage)
		return False

	#####################################################################################
	# Find the structure name, and add a blank entry in the overall structure dictionary
	curlyBraceEndIndex = curlyBraceStartIndex + matchingBraceDistance(tokenList[curlyBraceStartIndex:])
	
	if ";" not in tokenList[curlyBraceEndIndex+1:]:
		errorMessage = "ERROR in parseStructure() - for parentStructName = <"+parentStructName+">, no semicolon after ending curly brace - exiting!" 
		errorRoutine(errorMessage)
		return False
	else:
		nextSemicolonAfterCurlyBraceEndIndex = curlyBraceEndIndex+1 + tokenList[curlyBraceEndIndex+1:].index(";")

		# When we have the __attribute__ statement right after the closing "}", it is considered. Otherwise, it is ignored
		#  Allowed: struct  S { char c; short s, int i;} __attribute__((packed))Sa;
		#  Ignored: struct  S { char c; short s, int i;}                        Sa __attribute__((packed));
		# So, we need to find out exactly where the "valid" __attribute__ statements end (there might be multiple such statements)
		
		lastValidAttributeEndIndex = curlyBraceEndIndex
		while tokenList[lastValidAttributeEndIndex+1] == ATTRIBUTE_STRING :
			lastValidAttributeEndIndex = lastValidAttributeEndIndex+2+matchingBraceDistance(tokenList[lastValidAttributeEndIndex+2:nextSemicolonAfterCurlyBraceEndIndex])

		# Now, these are the indices of the various key items:
		
		# structDefinitionStartIndex 			- where the struct definition statement actually starts
		# structOrUnionTypeIndex 				- index of the field that contains the struct/union keyword
		# curlyBraceStartIndex					- self-explanatory
		# curlyBraceEndIndex					- self-explanatory
		# lastValidAttributeEndIndex			- this is the index of the token where (if any) valid post-"}" __attribute__ statements end 
		# nextSemicolonAfterCurlyBraceEndIndex	- self-explanatory

		if not (structDefinitionStartIndex <= structOrUnionTypeIndex < curlyBraceStartIndex < curlyBraceEndIndex < nextSemicolonAfterCurlyBraceEndIndex):
			errorMessage = "Error in parseStructure - we don't have structDefinitionStartIndex(%d) <= structOrUnionTypeIndex(%d) < curlyBraceStartIndex(%d) < curlyBraceEndIndex(%d) < nextSemicolonAfterCurlyBraceEndIndex (%d)"%(structDefinitionStartIndex, structOrUnionTypeIndex, curlyBraceStartIndex, curlyBraceEndIndex, nextSemicolonAfterCurlyBraceEndIndex)
			errorRoutine(errorMessage)
			return False
		else:
			# These are the "slots" (defined by a [start index, end index] where the __attribute__ statements might reside)
			# Observe that we deliberately put structDefinitionStartIndex-1 instead of just structDefinitionStartIndex, because in all other cases we cannot have the
			# __attribute__statement right on any of the start or end indices, but for structDefinitionStartIndex it might be the case
			attributeSlots = [[structDefinitionStartIndex-1, structOrUnionTypeIndex],[structOrUnionTypeIndex, curlyBraceStartIndex],[curlyBraceEndIndex,lastValidAttributeEndIndex]]
			
		
		# Handle all the attributes in all possible slots
		
		attributes = {}	# This is the structure-level dectionary that will store all the attributes from the various __attribute__ statements
		attributeIndicesStartEnd = {}	# We want to cache the <start index, end index (inclusive) > of each of the __attribute__ statements
		
		for startEndPair in attributeSlots:
			startIndex = startEndPair[0]
			endIndex = startEndPair[1]
			
			k = startIndex + 1
			while (k < endIndex):
				if tokenList[k] != ATTRIBUTE_STRING:
					k += 1
				else:
					PRINT("Currently processing tokenList = < %s >"%STR(tokenList[k:endIndex+1]))
					parseAttributeResult = parseAttribute(tokenList[k:endIndex+1])
					if parseAttributeResult[0] != True:
						errorMessage = "ERROR in parseStructure() after calling parseAttribute() for tokenList[k(%d):endIndex(%d) = <%s>]"%(k,endIndex,STR(tokenList[k:endIndex]))
						errorRoutine(errorMessage)
						return False
					else:
						d = parseAttributeResult[1]["distance"]
						attributeIndicesStartEnd[k]=k+1+d
						PRINT("parseAttributeResult[1] = ",parseAttributeResult[1])
						for (key, value) in parseAttributeResult[1].items():
							if key == ALIGNED_STRING and ALIGNED_STRING in getDictKeyList(attributes):
								attributes[key] = max(value,attributes[key])
							else:
								attributes[key] = value
						k = attributeIndicesStartEnd[k] + 1

		# Sanity check
		rightMostIndexForAttributeStatementEndTokenBeforeCurlyBraceStart = -99999999999999
		totalTokensConsumedByAttributeStatements = 0
		for (key, value) in attributeIndicesStartEnd.items():
			if tokenList[key:key+3] != [ATTRIBUTE_STRING,"(","("] or tokenList[value-1:value+1] != [")",")"]:
				errorMessage = "ERROR in parseStructure() while doing sanity check after calling parseAttribute(); tokenList[k(%d):value+1(%d) = <%s>]"%(key, value+1, STR(tokenList[key:value+1]))
				errorRoutine(errorMessage)
				return False
			# We also check which is the right-most __attribute__ statement within [structOrUnionTypeIndex, curlyBraceStartIndex]
			# The reason we do this is that if there is struct name, it must be the one right before the "{".
			# Remember that this construction below is not allowed:
			#
			#  struct S __attribute__((packed)){ char c; short s, int i;} Sa;
			if structOrUnionTypeIndex < key < curlyBraceStartIndex:
				totalTokensConsumedByAttributeStatements += attributeIndicesStartEnd[key] - key + 1
				if attributeIndicesStartEnd[key] > rightMostIndexForAttributeStatementEndTokenBeforeCurlyBraceStart:
					rightMostIndexForAttributeStatementEndTokenBeforeCurlyBraceStart = attributeIndicesStartEnd[key]

		structName = ""
		if totalTokensConsumedByAttributeStatements == 0:	# No __attribute__ statement between the struct and {
			PRINT ("No __attribute__ statement between the struct and {")
			if curlyBraceStartIndex == structOrUnionTypeIndex + 1:
				PRINT ("Anonymous struct/union")
			elif curlyBraceStartIndex == structOrUnionTypeIndex + 2:
				structName = tokenList[structOrUnionTypeIndex+1]
			else:
				errorMessage = "ERROR in parseStructure() for tokenList[structOrUnionTypeIndex(%d):curlyBraceStartIndex(%d)+1 = <%s>] - extra tokens other than the struct/union name between the struct/union and the \"{\""%(structOrUnionTypeIndex,curlyBraceStartIndex,STR(tokenList[structOrUnionTypeIndex:curlyBraceStartIndex+1]))
				errorRoutine(errorMessage)
				return False
		else:		# There are __attribute__ statement between the "struct" and "{"
			PRINT ("There are __attribute__ statement(s) between the struct and { that consume a total of ",totalTokensConsumedByAttributeStatements,"tokens")
			if totalTokensConsumedByAttributeStatements == curlyBraceStartIndex - structOrUnionTypeIndex - 1:	# Nothing other than __attribute__ statements, if any
				PRINT ("Anonymous struct/union")
			elif totalTokensConsumedByAttributeStatements < curlyBraceStartIndex - structOrUnionTypeIndex - 1:
				# So there is at least one non-attribute token between the "struct" and "{"
				if rightMostIndexForAttributeStatementEndTokenBeforeCurlyBraceStart == curlyBraceStartIndex - 1:
					errorMessage = "ERROR in parseStructure() for tokenList[structOrUnionTypeIndex(%d):curlyBraceStartIndex(%d)+1 = <%s>] - the struct name must be just before the \"{\""%(structOrUnionTypeIndex,curlyBraceStartIndex,STR(tokenList[structOrUnionTypeIndex:curlyBraceStartIndex+1]))
					errorRoutine(errorMessage)
					return False
				elif totalTokensConsumedByAttributeStatements + 1 < curlyBraceStartIndex - structOrUnionTypeIndex - 1:
					errorMessage = "ERROR in parseStructure() for tokenList[structOrUnionTypeIndex(%d):curlyBraceStartIndex(%d)+1 = <%s>] - extra token just before the \"{\""%(structOrUnionTypeIndex,curlyBraceStartIndex,STR(tokenList[structOrUnionTypeIndex:curlyBraceStartIndex+1]))
					errorRoutine(errorMessage)
					return False
				elif totalTokensConsumedByAttributeStatements + 1 == curlyBraceStartIndex - structOrUnionTypeIndex - 1:
					if rightMostIndexForAttributeStatementEndTokenBeforeCurlyBraceStart == curlyBraceStartIndex - 2:
						structName = tokenList[curlyBraceStartIndex-1]
					else:
						errorMessage = "ERROR in parseStructure() for tokenList[structOrUnionTypeIndex(%d):curlyBraceStartIndex(%d)+1 = <%s>] - No idea why I am here"%(structOrUnionTypeIndex,curlyBraceStartIndex,STR(tokenList[structOrUnionTypeIndex:curlyBraceStartIndex+1]))
						errorRoutine(errorMessage)
						return False
				
		PRINT ("After parsing all the struct-level __atribute__ statements for structName = <",structName,">, the attribute is ", attributes)
		
		# Find out if it is named structure or not. The way we find it is that we assume there might be __attribute__ statements betwen the structOrUnionTypeIndex
		# and the curlyBraceStartIndex. However, if it is a named struct/union, the name must be the very token right before 
		
		structNameAlreadyDeclared = False
		
		
		if structName != "":	# Named struct declaration
			if structuresAndUnionsDictionary and structName in getDictKeyList(structuresAndUnionsDictionary):
				if "components" in getDictKeyList(structuresAndUnionsDictionary[structName]) and structuresAndUnionsDictionary[structName]["components"] != []:
					structNameAlreadyDeclared = True
					PRINT ("ERROR in parseStructure()" )
					errorMessage = "ERROR in parseStructure(): structName %s already exists as another %s!"%(structName,structuresAndUnionsDictionary[structName]["type"])
					errorRoutine(errorMessage)
					return False
				else:
					# Handle the case of empty declarations. This is to handle the case of circular struct definition in C
					# For example, this is legal is C:
					# 										struct A { struct B * b;};
					# 										struct B { struct A * a;};
					#
					PRINT ("struct ", structName, "already declared, but NOT its components" )
				
			elif typedefs and (structName in getDictKeyList(typedefs)):
				PRINT ("ERROR in parseStructure()" )
				errorMessage = "structName %s already exists as another already-declared typedef %s!"%(structName,STR(typedefs[structName]))
				errorRoutine(errorMessage)
				return False
		elif structName == "":	# Anonymous struct definition
			PRINT ("WARNING: Anonymous structure/union declaration!!" )
			if structuresAndUnionsDictionary:
				totalNumberOfEmptyStructsTillNow = 0
				for key in structuresAndUnionsDictionary.keys():
					if (len(key) > len(anonymousStructPrefix)) and (key[:len(anonymousStructPrefix)] == anonymousStructPrefix):
						num = int(key[len(anonymousStructPrefix):])
						if num > totalNumberOfEmptyStructsTillNow:
							totalNumberOfEmptyStructsTillNow = num
				structName = anonymousStructPrefix + STR(totalNumberOfEmptyStructsTillNow+1)
			else:
				structName = anonymousStructPrefix + "1"
		else:
			PRINT ("ERROR - should have never come here in parseStructure()" )
			PRINT ("tokenList[i] = tokenList[",i,"] = ",tokenList[i]," tokenList =",tokenList)
			errorMessage = "ERROR in parseStructure() figuring out if the struct/union is named or anonymous - should have never come here "
			errorRoutine(errorMessage)
			sys.exit()
			
		# Each value of this structuresAndUnionsDictionary is a dictionary itself. The value dictionary is of this format: 
		# "type" : "struct/union", "size":size, "components":[[variable1 name, variable size, variable declaration statement, variable description],...]}
		
		#The reason we create a blank entry right away is that there might be a pointer to a struct itself inside its member list
		if not structNameAlreadyDeclared:
			structuresAndUnionsDictionary[structName] = {"type":structOrUnionType}
			structuresAndUnionsDictionary[structName]["parentStructName"] = parentStructName
			structuresAndUnionsDictionary[structName]["components"] = []
		if attributes:
			structuresAndUnionsDictionary[structName]["attributes"] = attributes
		
		i = curlyBraceStartIndex + 1
		
		structSizeBytes = 0

		usingDummyVariable = False
		
		############################################################################
		# Parse all the individual members of this struct/union
		while i < curlyBraceEndIndex:
			if ";" not in tokenList[i:curlyBraceEndIndex]:
				PRINT ("No semicolon in tokenList[i:curlyBraceEndIndex] = tokenList[",i,":",curlyBraceEndIndex,"] = ",tokenList[i:curlyBraceEndIndex] )
				errorMessage = "ERROR in parseStructure() while parsing - every %s member declaration must end with a semicolon - exiting"%structOrUnionType
				errorRoutine(errorMessage)
				return False
			else:
				#TO-DO: Empty declaration statement (semicolon only) for struct?
				nextSemicolonIndex = i+1 + tokenList[i+1:curlyBraceEndIndex].index(";")
				
			structDefinedHere = False	# Default value for nested structure definition
			
			# Nested structure declaration. Remember that there might be __attribute__ statements all round
			if ('{' in tokenList[i+1:nextSemicolonIndex]) and (('struct' in tokenList[i:nextSemicolonIndex]) or ('union' in tokenList[i:nextSemicolonIndex])):	
				nestedStructureCurlyBraceStartIndex = i+1 + tokenList[i+1:].index("{")
				nestedStructOrUnionType = "struct" if "struct" in tokenList[i:nestedStructureCurlyBraceStartIndex] else "union"
				matchingBraceDistanceNested = matchingBraceDistance(tokenList[nestedStructureCurlyBraceStartIndex:])
				if matchingBraceDistanceNested <1:
					errorMessage = "Error in parseStructure() for structName <"+structName+"> - missing \"}\" for nested "+nestedStructOrUnionType+" declaration"
					errorRoutine(errorMessage)
					return False
				else:
					nestedStructureCurlyBraceEndIndex = nestedStructureCurlyBraceStartIndex + matchingBraceDistanceNested
				
				# The result is the structName, which is particularly useful when it is an Anonymous structure
				parseStructureResult = parseStructure(tokenList, nestedStructureCurlyBraceStartIndex, structName, level+1)
				
				if parseStructureResult == None:
					errorMessage = "Error coding parseStructure() for structName <"+structName+"> - return value is None"
					errorRoutine(errorMessage)
					return False
				elif parseStructureResult == False:
					errorMessage = "Error calling parseStructure() for nested struct - return value is None"
					errorRoutine(errorMessage)
					return False
				else:
					nestedStructName = parseStructureResult
					PRINT ("Parsed upto tokenList[",i,"] = ",tokenList[i],"after parsing nested",nestedStructOrUnionType )
					if ';' not in tokenList[nestedStructureCurlyBraceEndIndex+1:curlyBraceEndIndex]:
						errorMessage = "Error in parseStructure(): No semicolon following nested %s declaration"%nestedStructOrUnionType
						errorRoutine(errorMessage)
						return False
					structDefinedHere = True
					nextSemicolonIndex = nestedStructureCurlyBraceEndIndex+1 + tokenList[nestedStructureCurlyBraceEndIndex+1:curlyBraceEndIndex].index(";")
					memberDeclarationStatement = tokenList[i:nestedStructureCurlyBraceStartIndex]
					if nestedStructName.startswith(anonymousStructPrefix):	# Anonymous nested structure
						memberDeclarationStatement.append(nestedStructName)	# This is actually the Anonymous struct/union name
						
					# nestedLastValidAttributeEndIndex	- there might be __attribute__ statements after the closing "}" for a nested struct/union
					# We need to know exactly where that ends is because the struct variables declaration (not the member variables) start right after that.
					nestedLastValidAttributeEndIndex = nestedStructureCurlyBraceEndIndex
					while tokenList[nestedLastValidAttributeEndIndex+1] == ATTRIBUTE_STRING :
						nestedLastValidAttributeEndIndex = nestedLastValidAttributeEndIndex+2+matchingBraceDistance(tokenList[nestedLastValidAttributeEndIndex+2:nextSemicolonIndex])

					# For the consistency, add the __attribute__ statements after the "}"
					memberDeclarationStatement.extend(tokenList[nestedStructureCurlyBraceEndIndex+1:nestedLastValidAttributeEndIndex+1])

					# Now, since this is a synthetic statement, we know that all the __attribute__ statements have already been processed.
					# There is no need to include them in the synthetic declaration statement further. Hence, remove them.
					
					while True:
						if ATTRIBUTE_STRING not in memberDeclarationStatement:
							break
						else:
							PRINT ("Before removing __attribute__ statements, memberDeclarationStatement = <",flattenList(memberDeclarationStatement),">")
							begin = memberDeclarationStatement.index(ATTRIBUTE_STRING)
							end = begin+1+matchingBraceDistance(memberDeclarationStatement[begin+1:])
							del memberDeclarationStatement[begin:end+1]
							PRINT ("After removing __attribute__ statements, memberDeclarationStatement = <",flattenList(memberDeclarationStatement),">")
					
					numFakeEntries = len(memberDeclarationStatement) # We have to capture it right here, because i will point to the first token after nestedLastValidAttributeEndIndex
					
					# Remember, there might be __attribute__ statements after the nestedLastValidAttributeEndIndex too. But they will NOT apply to the nested struct.
					# They might apply to the individual variables.
					memberDeclarationStatement.extend(tokenList[nestedLastValidAttributeEndIndex+1:nextSemicolonIndex+1])
					
					
#					numFakeEntries = 2	# Why 2? Possible bug
#					i = nestedStructureCurlyBraceEndIndex + 1
					i = nestedLastValidAttributeEndIndex + 1
					# This is special case where we do not have the struct member declaration.
					if tokenList[i] == ';':	# Only structure definition, no declaration
						usingDummyVariable = True
						del memberDeclarationStatement[-1]	# remove the semicolon 
						dummyVariableCount += 1
						dummyVariableName = dummyVariableNamePrefix + STR(dummyVariableCount)
						memberDeclarationStatement.append(dummyVariableName)
						memberDeclarationStatement.append(';')	# Put back the semicolon
					else:
						usingDummyVariable = False
			else:
				memberDeclarationStatement = tokenList[i:nextSemicolonIndex+1]
				numFakeEntries = 0
			# End nested structure handling
			
			# Find the data type. It might be primitive, or derived
			dataTypeIndex = 0
			while memberDeclarationStatement[dataTypeIndex] in ('auto','register','static','extern', 'const','volatile'):	# What about typedef? Possible bug
				dataTypeIndex += 1
			PRINT ("For dataTypeIndex = ",dataTypeIndex," and i =",i,"memberDeclarationStatement[dataTypeIndex] = ",memberDeclarationStatement[dataTypeIndex])

			# BEGIN The user used some builtin typedef, handle that case
			if (memberDeclarationStatement[dataTypeIndex] not in getDictKeyList(typedefs)) and (memberDeclarationStatement[dataTypeIndex] in getDictKeyList(typedefsBuiltin)):
				list2Parse = typedefsBuiltin[memberDeclarationStatement[dataTypeIndex]] # This will happen only the first time, after that it will become part of typedefs
				parsed5tupleList = parseVariableDeclaration(list2Parse)

				if parsed5tupleList == False:
					errorMessage = "ERROR in parseStructure() after calling parseVariableDeclaration(list2parse) for list2parse = "+ STR(list2parse)
					errorRoutine(errorMessage)
					return False
				
				PRINT ("Builtin typedef declaration",parsed5tupleList, "parsed" )
				for item in parsed5tupleList:
					typeSpecifierEndIndex = item[4]["typeSpecifierEndIndex"]
					variableDeclarationStatement = item[2]
					PRINT ("Main variable name is ",item[0],"of size",item[1],"and it is located at relative index of ",item[3],"inside the variable declaration statement",item[2],", where the base type specifier ends at index =", )
					if usingDummyVariable:
						pass
					elif list2Parse[item[3]]!=item[0]:
						errorMessage = "ERROR in parseStructure() after parsing user's usage of builtin type"+memberDeclarationStatement[dataTypeIndex] +"- list2Parse[item[3]] = " + STR(list2Parse[item[3]]) + " !=item[0]=" + STR(item[0])
						errorRoutine(errorMessage)
						return False
					else:
						variableNameIndex = item[3]
					
					globalTokenListIndex = -100000
					variableDescriptionExtended = item[4]
					variableDescriptionExtended["globalTokenListIndex"]=globalTokenListIndex 
					variableDescriptionExtended["level"]=level+1 
					variableDescriptionExtended["variableId"] = totalVariableCount
					totalVariableCount += 1
					variableDeclarations.append([item[0],item[1],item[2],variableNameIndex,variableDescriptionExtended])
			# END The user used some builtin typedef, handle that case
				

			# If a structure member uses a derived type, we need to replace the memberDeclarationStatement with an expanded one
			memberDeclarationStatementAltered = False	# Starting with a default value
			originalMemberDeclarationStatement = memberDeclarationStatement
			
			if memberDeclarationStatement[dataTypeIndex] in getDictKeyList(typedefs):
				memberDeclarationStatement = convertDerivedTypeDeclarationIntoBaseTypeDeclaration(memberDeclarationStatement,dataTypeIndex)
				memberDeclarationStatementAltered = True
			
			PRINT("originalMemberDeclarationStatement =",originalMemberDeclarationStatement)
			PRINT ("memberDeclarationStatement =",memberDeclarationStatement)
				
			PRINT ("Going to parse from tokenList[",i,"through",nextSemicolonIndex,"] (both indices included) = ",memberDeclarationStatement )
			
			# Parse the individual member declaration statement
			parsed5tupleList = parseVariableDeclaration(memberDeclarationStatement)
			
			if parsed5tupleList == False:
				PRINT ("ERROR in parseStructure() for struct after calling parseVariableDeclaration(memberDeclarationStatement) for memberDeclarationStatement =",memberDeclarationStatement )
				return False
			PRINT ("struct/union/regular declaration",parsed5tupleList, "parsed" )
			
			existingStructComponentNames = []	# We want to ensure that you cannot re-declare the same variable twice within the same structure
			if structuresAndUnionsDictionary[structName]["components"]:
				for structItem in structuresAndUnionsDictionary[structName]["components"]:
					existingStructComponentNames.append(structItem[0])
				PRINT ("existingStructComponentNames =",existingStructComponentNames)
				
			variableFoundWithDataOverlapWithStructMembers = False
				
			for item in parsed5tupleList:
				PRINT (structOrUnionType,structName,"has the following declarations after it" )
				PRINT ("Main variable name is ",item[0],"of size",item[1],"and it is located at relative index of ",item[3],"inside the variable declaration statement",item[2] )
				if item[0] in existingStructComponentNames:
					PRINT (item[0],"already appears in existingStructComponentNames =",existingStructComponentNames)
					errorMessage = "ERROR in parseStructure(): component "+item[0]+" has already been declared (cannot be re-declared within the same structure/union)"
					errorRoutine(errorMessage)
					return False
				# Each member of the list follows exactly the same format as the parsed5tupleList, with one key addition - the 6th item.
				# This 6th member now represents the absolute index (within the tokenList) of the variable name.
				
				if memberDeclarationStatementAltered == False:
					if not usingDummyVariable and item[0] != dummyZeroWidthBitfieldNamePrefix and tokenList[i+item[3]-numFakeEntries]!=item[0]:
						PRINT ("ERROR in parseStructure() - for i=",i,"tokenList[i+item[3]-numFakeEntries] = tokenList[",i,"+",item[3],"-",numFakeEntries,"] =",tokenList[i+item[3]-numFakeEntries],"!=item[0]=",item[0] )
						return False
					else:
						PRINT ("In parseStructure(), - for i=",i,"tokenList[i+item[3]-numFakeEntries] = tokenList[",i,"+",item[3],"-",numFakeEntries,"] =",tokenList[i+item[3]-numFakeEntries],"matches item[0]=",item[0] )
						globalTokenListIndex = i+item[3]-numFakeEntries
						variableNameIndex = item[3]
						
				elif memberDeclarationStatementAltered == True: 	# Derived type
					PRINT ("i =",i,"dataTypeIndex =",dataTypeIndex,"tokenList[dataTypeIndex] =",tokenList[dataTypeIndex])
					variableDeclarationStartIndex = i	# Since we do not allow typedef within struct member definition, the very first term should be the derived type
#					variableDeclarationStartIndex = dataTypeIndex	# Since we do not allow typedef within struct member definition, the very first term should be the derived type
					typeSpecifierEndIndex = item[4]["typeSpecifierEndIndex"]
					variableDeclarationStatement = item[2]
					PRINT ("Main variable name is ",item[0],"of size",item[1],"and it is located at relative index of ",item[3],"inside the variable declaration statement",item[2],", where the base type specifier ends at index =", )
#					if tokenList[i] in getDictKeyList(typedefs):			# MannaManna
					if tokenList[i+dataTypeIndex] in getDictKeyList(typedefs):
						PRINT ("We modified the declaration statement, so we know that position index of the declared variable", item[0],"would not match (hence not checking it)" )
						if item[0]==dummyZeroWidthBitfieldNamePrefix:
							variableNameIndex = originalMemberDeclarationStatement.index(':')
						else:
							variableNameIndex = originalMemberDeclarationStatement.index(item[0])
					elif usingDummyVariable:
						# Since the dummyvariable will be like struct nestedStructName dummyVariable, its position # should be always 2 (remember, typedefs are not allowed)
						# TO-DO - accommodate the case where other cases like volatile / static / extern etc. qualifiers would precede the nested struct definition.
						# Int that case, the variableNameIndex might be more than 2.
						variableNameIndex = 2
					elif item[0] != dummyZeroWidthBitfieldNamePrefix and tokenList[variableDeclarationStartIndex+item[3]]!=item[0]:
						errorMessage = "ERROR in parseStructure() - for variableDeclarationStartIndex = "+ STR(variableDeclarationStartIndex) + " tokenList[variableDeclarationStartIndex+item[3]] = " + STR(tokenList[variableDeclarationStartIndex+item[3]]) + " !=item[0]=" + STR(item[0])
						errorRoutine(errorMessage)
						return False
					else:
						variableNameIndex = item[3]
					globalTokenListIndex = variableDeclarationStartIndex+variableNameIndex
				
				variableId = totalVariableCount
				
				# Here is the final place where the individual structure memebers gets added to the variableDeclarations and structuresAndUnionsDictionary
				variableDescriptionExtended = item[4]
				variableDescriptionExtended["globalTokenListIndex"]=globalTokenListIndex
				variableDescriptionExtended["parentVariableType"]=[structOrUnionType,structName]
#				variableDescriptionExtended["parentVariableName"]=structName
				variableDescriptionExtended["level"]=level+1
				variableDescriptionExtended["variableId"] = variableId
				
				if not variableFoundWithDataOverlapWithStructMembers and structDefinedHere and variableDescriptionExtended["datatype"] == nestedStructName:
					variableDescriptionExtended["DataOverlapWithStructMembers"] = True 
					variableFoundWithDataOverlapWithStructMembers = True
				else:
					variableDescriptionExtended["DataOverlapWithStructMembers"] = False
					
				variableDeclarations.append([item[0],item[1],item[2],variableNameIndex,variableDescriptionExtended])
				
				structuresAndUnionsDictionary[structName]["components"].append(item)

				totalVariableCount += 1

			i = nextSemicolonIndex + 1
		# END-WHILE Parse all the individual members of this struct/union
		
		
		
		
		###############################################################################################################################################################
		#
		#           P A C K E D        and    A L I G N E D     ( via __attribute__ )
		#
		###############################################################################################################################################################
		#
		#
		#  These two directives can be added at the individual member level of a structure, or can be just applied at the struct level (where it will apply to all the members)
		#
		#  Basically, what packed directive tells is that - ignore the natual alignment of the datatype (for example 2 bytes for a short, 4 bytes for an int) and 
		#  just start "packing" the variable exactly after the previous variable ends (do not allow the compiler to add any padding in between).
		#
		#  The aligned(N) directive, where N must be 1/2/4/8/16 (basically a proper power of 2), on the other hand, ensures two things. 
		#  1. The variable must be start from the natural boundary of the mentioned aligned(N).
		#  2. It must take at least N bytes of space (paddings may need to be added). It does not care if the next member starts packing right on top of the padding,
		#     as long it does not reduce the space allocated by the aligned() statement.
		#  3. If the N in aligned(N) is smaller than the native size of the member, the native size overrides N. E.g., if you have short s __attribute__ ((aligned(1)));
		#     then the aligned(1) is ignored. Only way to make the short align to a 1-byte boudary is by using the __attribute__((packed)) or #pragma pack(1)
		#
		#  If there are conflicting directives, e.g. __attribute__((packed, aligned)), then aligned wins. It does not matter if the packed is at the member-level or 
		#  at the struct-level, it will not be able to override aligned. However, #pragma pack can override aligned by reducing it (it cannot increase).
		#
		#  The __attribute_(()) can be mentioned at the beginning of the statement (before even struct), right after the struct but before the struct name (if named),
		#  or right after the ending curly brace.
		#
		# Declaring it at the struct level:
		#
		#  Allowed:   __attribute__((packed)) struct                         S                        { char c; short s, int i;}                        Sa;
		#  Allowed:                           struct __attribute__((packed)) S                        { char c; short s, int i;}                        Sa;
		#  Not allowed:                       struct                         S __attribute__((packed)){ char c; short s, int i;}                        Sa;
		#  Allowed:                           struct                         S                        { char c; short s, int i;} __attribute__((packed))Sa;
		#  Ignored:                           struct                         S                        { char c; short s, int i;}                        Sa __attribute__((packed));
		#
		# Declaring it at the struct member level:
		#
		#  Allowed:   __attribute__((packed)) int                            i1                        ,                        i2;	<== "packed" applies to both i1 and i2
		#  Allowed:                           int   __attribute__((packed))  i1                        ,                        i2;	<== "packed" applies to both i1 and i2
		#  Allowed:                           int                            i1 __attribute__((packed)),                        i2;	<== "packed" applies to only i1 but not i2
		#  Allowed:                           int                            i1                        , __attribute__((packed))i2;	<== "packed" applies to only i2 but not i1
		#
		#  When you have multiple __attibute__ parameters, you can mention them in 3 ways.
		#    1. Comma-separated. Like __attribute__((packed, aligned))
		#    2. Space-separated. Like __attribute__((packed  aligned))
		#    3. Separate entry for each parameter. Like struct __attribute__((packed)) {int a;} __attribute__((aligned)). But each entry can only be in one of the allowed places.
		#
		#   Also, to ensure that it accidentally does not collide with any macro names, instead of "packed", one can also use "__packed__" (and similarly for other attributes).
		
		# An __attribute__((packed)) statment simply brings the alignment to 1.
		# An __attribute__((align(m))) statement causes a member variable to align to a number that LARGER than its current alignment. 
		# Suppose the natural size (and thus natural alignment) of a struct member is s, and we have an aligned(m) statement.
		#
		# if s < m, then irrespective of whether this is any packed statement, the alignment is increased to m. 
		#    Because even when the packed statement brings the alignment down to 1, the aligned(m) then increases it to m.
		#    So, both the size and alignment for this member increases, leading to traling padding (which may be reused by next member), and possibly leading padding.
		# if m < s, then it depends on whether this is any packed statement (at either the member-level or the struct-level, either will do).
		#  - if there is a packed statement, then the alignment is first reduced to 1 from s. Then align(m) increases it to m.
		#    So, overall the size remains the same as s, but the alignment gets reduced to m. This may lead to some leading pads (if m >1), but no trailing pads.
		#  - if there is NO packed statement, then alignment remains at s, and since an align(m) can only "increase-to-m (never reduce)", 
		#    the align(m) is effectively ignored, and the resulting member-level alignment as well as size is s. This may lead to leading pads (if s > 1).
		#
		# #pragma pack(n) is a Microsoft directive that was back-ported into gcc. It simply ensures that maximum alignment of each struct member is n.
		# It does not say anything about packing. So, do NOT take it as an equivalent of putting a __attribute__((packed, aligned(m))) to every struct member.
		# So, #pragma pack(n) only reduces the alignment to n. It never increases it to n.
		#
		# So, the rule of the mix of #pragma pack(n), __attribute__((packed)) and , __attribute__(aligned(m))) is that:
		# First calculate the effective size and alignment just considering the natural size, packed and aligned(m)
		# If the resulting alignment is > n, reduce it to n.
		# If the resulting size is > n, reduce it to n. However, if n < s (the natural size), then effective size is s.
		
		#
		# Here's a summary of the differences:
		#
		#  - #pragma pack applies to every structure definition placed after where it is inserted (or until another #pragma pack overrides it), 
		#    while GCC __attribute__s are defined locally to a type;
		#  - #pragma pack is less fine-grained than attributes: it cannot be applied to only a few members of a struct.  
		#     In practice, however, this is rarely an issue, since you'll rarely need different alignment and packing settings for the members of a same struct.
		#
		# See https://docs.microsoft.com/en-us/cpp/preprocessor/pragma-directives-and-the-pragma-keyword?view=vs-2019 
		# See https://docs.microsoft.com/en-us/cpp/preprocessor/pack?view=vs-2019
		#
		# As per https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.2.0/com.ibm.zos.v2r2.cbclx01/pragma_pack.htm
		# 
		#  The #pragma pack directive modifies the current alignment rule for only the members of structures whose declarations follow the directive. 
		#  It does not affect the alignment of the structure directly, but by affecting the alignment of the members of the structure, 
		#  it may affect the alignment of the overall structure.
		#
		#  The #pragma pack directive cannot increase the alignment of a member, but rather can decrease the alignment. For example, for a member with data type of short, 
		#  a #pragma pack(1) directive would cause that member to be packed in the structure on a 1-byte boundary, while a #pragma pack(4) directive would have no effect.
		#
		# As per https://gcc.gnu.org/onlinedocs/gcc-4.4.4/gcc/Structure_002dPacking-Pragmas.html
		# 
		# For compatibility with Microsoft Windows compilers, GCC supports a set of #pragma directives which change the maximum alignment of members of structures 
		# (other than zero-width bitfields), unions, and classes subsequently defined. The n value below always is required to be a small power of two and 
		# specifies the new alignment in bytes.

		#  #pragma pack(n) 			simply sets the new alignment. Must be 1, 2, 4, or 8
		#  #pragma pack() 			sets the alignment to the one that was in effect when compilation started (see also command line option -fpack-struct[=<n>] see Code Gen Options).
		#							So, here this is equivalent to #pragma pack(ALIGNED_DEFAULT_VALUE), or setting pragmaPackCurrentValue = ALIGNED_DEFAULT_VALUE
		#  #pragma pack(push[,n]) 	pushes the current alignment setting on an internal stack and then optionally sets the new alignment.
		#  #pragma pack(pop) 		restores the alignment setting to the one saved at the top of the internal stack (and removes that stack entry). 
		#
		# Note that #pragma pack([n]) does not influence this internal stack; thus it is possible to have #pragma pack(push) followed by multiple #pragma pack(n) instances and 
		# finalized by a single #pragma pack(pop). 	
		#
		# MOST IMPORTANT: The alignment of a member is on a boundary that's either a multiple of n, or a multiple of the size of the member, whichever is smaller.
		#
		#
		#  Some examples below.
		#   _____________________________________________________________________________________________________________________________________________________
		#  |  struct A {                                     | sizeof(A) = 6, because the compiler will add a 1-byte padding after c1. It will also add a 1-byte
		#  |        char c1;                                 | padding at the end of the struct after c2.
		#  |        short s;                                 |
		#  |        char c2;                                 |
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct __attribute__((packed)) B {             | sizeof(B) = 4, because now the compiler will pack all the members as tightly as possible.
		#  |        char c1;                                 | If c2 were a short, its size would have been 5.
		#  |        short s;                                 |
		#  |        char c2;                                 |
		#  |  };                                             |
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct C {                                     | sizeof(C) = 4, because now the compiler will pack only the member s as tightly as possible.
		#  |        char c1;                                 | And for char variables, the compiler does not need (and therefore ignores) any 
		#  |        short s __attribute__((packed));         | __attribute__((packed)), since a char can start from any byte boundary.
		#  |        char c2;                                 | However, if instead of "char c2;" we had a "char c2[2];", in that case the sizeof(C) would 
		#  |  };                                             | be 6 since the compiler would align it to a 2-byte-boundary.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct D {                                     | sizeof(D) = 18, because now the compiler will pack only the member i[4] as tightly as possible.
		#  |        char c1;                                 | 
		#  |        int i[4] __attribute__((packed));        | 
		#  |        char c2;                                 |  
		#  |  };                                             | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct E  {                                    | sizeof(E) = 6, because now the compiler will pad 1 bytes at the end.
		#  |        short s[2];                              | Observe that the compiler is decide to align the final struct boundary at a 2-byte boundary,
		#  |        char c;                                  | because that is the largest alignment among all the struct members. Once again, it is not 
		#  |  };                                             | the size of the WHOLE array, it is the size of the "base" member of the array.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct F  {                                    | sizeof(F) = 8, because now the compiler will pad 3 bytes at the end. Compare it with the above.
		#  |        int i;                                   | Both "short s[2];" and "int i;" take exactly 4 bytes, yet for the former the compiler is 
		#  |        char c;                                  | adhering to a 2-byte-boudary while for the latter it is adhering to a 4-byte boudary,
		#  |  };                                             | because that is now the largest alignment among all the struct members.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct __attribute__((packed)) G {             | sizeof(G) = 5, because the packed will now cause the compiler to not add the trailing pads.
		#  |        int i;                                   | 
		#  |        char c;                                  |  
		#  |  };                                             | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct __attribute__((aligned(2))) H {         | sizeof(H) = 2, because unlike the __attribute__((packed)), when you place the __attribute__((aligned))
		#  |        char c1;                                 | at the struct definition level (NOT at the struct member level), the aligned attribute does NOT apply
		#  |        char c2;                                 | to each individual struct member. Because if it did, we would get sizeof(H) = 4.
		#  |  };                                             | Instead, it will apply to the "overall" structure length.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct __attribute__((aligned(2))) I {         | sizeof(I) = 4, because unlike the __attribute__((packed)), when you place the __attribute__((aligned))
		#  |        char c1;                                 | at the struct definition level (NOT at the struct member level), the aligned attribute does NOT apply
		#  |        char c2;                                 | to each individual struct member. Because if it did, we would get sizeof(H) = 4.
		#  |        char c3;                                 | Instead, it will apply to the "overall" structure length. So, out of the 4 byets, the last byte is pad.
		#  |  };                                             |
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct  J {                                    | sizeof(J) = 4, because even though the c2 will start (and end) at a 2-byte boundary (2nd byte is now pad), 
		#  |        char c1;    // 1-byte padding after c1   | it does not "prohibit" the next struct member (c3) to occupy/overlay the 1-byte padding after c2.
		#  |        char c2 __attribute__((aligned(2)));     | Remember that aligned(2) only ensures that the variable will start at a boundary that will
		#  |        char c3;  // c3 overlaps c2's padding    | align to a 2-byte boudary, and wil occupy "at least" 2 bytes. So, you can technically put an
		#  |  };                                             | __attribute__((aligned(2))) against an integer, it will not error out.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct  K {                                    | sizeof(K) = 6, not 5, inspite of the packed attributed being applied to the whole struct (and thus all members).
		#  |        char c1; //1-byte paddings after c1 & c2 | Out of these 6 bytes, the second and the last bytes are the padding (C3 occupies fourth and fifth bytes).
		#  |        char c2 __attribute__((aligned(2)));     | This also illustrates one vital property of aligned - the moment you apply to any of the struct member
		#  |        char c3[2];                              | variables, it also applies to the overall struct itself.
		#  |  }__attribute__((packed));                      | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct L  {                                    | sizeof(L) = 4, not 8. Because the aligned statement applied on the whole array size, not the individual
		#  |        short s[2] __attribute__((aligned(4)));  | array element. So, two shorts fit in a 4-byte nicely.
		#  |  };                                             | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct M  {                                    | sizeof(M) = 12. Because the aligned statement works on the whole array size, not the individual
		#  |        char c1; //3 bytes of padding after this | array element. So, there is a 3-byte padding before s[3] since it can only start at a 4-byte alignment, 
		#  |        short s[3] __attribute__((aligned(4)));  | but after the 3 shorts occupy 6 bytes, we still have 2 bytes of trailing padding left which are
		#  |        char c2[2]; //fits into the padding b4   | nicely utilized by the char c2[2];
		#  |  };                                             | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct A1{                                     | sizeof(A1) = 12, because now the compiler will pack int i2 from its natural alignement (4),
		#  |     int i1;                                     | So there will be a pad of 2 bytes before i2.
		#  |     short s;                                    |
		#  |     int i2;                                     |  
		#  |  };                                             | 
		#  |______________|__________________________________|_____________________________________________________________________________________________________
		#  |   struct A2 {                                   | sizeof(A2) = 12, because the compiler will still pack int i1 from its natural alignement (4),
		#  |         short s1;                               | So there will be a pad of 2 bytes before i1. 
		#  |         int i1 __attribute__((aligned(2)));     |
		#  |         short s2;                               | Observe that by attempting to reduce the alignment of i1 will not work since the intended alignement 
		#  |    };                                           | of 2 bytes is smaller than the natural size of the i1. So, in absense of a packed statement, 
		#  |                                                 | the aligned attribute statement will be ignored. Align only increases, never decreases.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct  __attribute__((packed)) A3{            | sizeof(A1) = 10, because now the compiler will pack int i2 from the 7th byte,
		#  |     int i1;                                     | So there will be no pads. Once we use the __attribute__((packed)) at the struct-level,
		#  |     short s;                                    | it will apply to each of the member variables, making each memeber's alignment to 1.
		#  |     int i2;                                     | Thus, the overall struct-level alignment = max (1,1,1) = 1. 
		#  |  };                                             | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct A4 {                                    | sizeof(A1) = 12, because now even though the compiler will pack int i2 from the 7th byte,
		#  |     int i1;                                     | we are using the __attribute__((packed)) at the member-level, not at the struct-level.
		#  |     short s;                                    | Therefore, the the overall struct-level alignment is still the maximum among all the members,
		#  |     int i2 __attribute__((packed));             |  = max(4,2,1) = 4. 
		#  |  };                                             | Thus, the overall struct size must be a multiple of 4, cause 2 bytes padding at end.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |                                                 | sizeof(B) = 8, because the compiler will calculate the struct-level alignment to be still the 
		#  |  struct B {                                     | maximum of all individual member-level alignments. The __attribute__((aligned(2))) will be ignored,
		#  |        int i __attribute__((aligned(2)));       | because in absense of a member-level or struct-level packed statement, you cannot apply the 
		#  |        short s;                                 | alignment if it were SMALLER than the natural size. In order to pack at a smaller alignment than
		#  |  };                                             | its natural alignment, you absolutely need a packed statement. Remember than align only increases.
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |                                                 | sizeof(B) = 6, because the compiler will calculate the struct-level alignment to be the 
		#  |  struct B {                                     | maximum of all individual member-level alignments. The __attribute__((aligned(2))) will now work,
		#  |    int i __attribute__((packed, aligned(2)));   | because now we have a member-level packed statement. 
		#  |    short s;                                     | Note that it is immaterial that the int i will pack from byte 0, which is still 4-byte-aligned.
		#  |  };                                             | Struct-level alignment = max(max(min(1,4),2), 2) = 2
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |                                                 | sizeof(B) = 8, because the compiler will calculate the struct-level alignment to be the 
		#  |  struct B {                                     | maximum of all individual member-level alignments. The __attribute__((aligned(2))) will now work,
		#  |    int i   __attribute__((packed, aligned(2))); | because now we have member-level packed statements. 
		#  |    short s __attribute__((packed, aligned(1))); | So, struct-level alignment = max (2, 1, 1) = 2. Hence there is going to be a 1-byte padding at the end.
		#  |    char c;                                      |
		#  |  };                                             | 
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 7, because the compiler will calculate the struct-level alignment to be the 
		#  |    int i   __attribute__((packed, aligned(1))); | maximum of all individual member-level alignments. The __attribute__((aligned())) will now work,
		#  |    short s __attribute__((packed, aligned(1))); | because now we have member-level packed statements. 
		#  |    char c;                                      | So, struct-level alignment = max (1, 1, 1) = 1. Hence there is going to be no padding at the end.
		#  |  };                                             | 
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 8, because the compiler will calculate the struct-level alignment to be the 
		#  |    int i   __attribute__((packed, aligned(1))); | maximum of all individual member-level alignments. The __attribute__((aligned())) will now work,
		#  |    short s __attribute__((packed, aligned(1))); | because now we have member-level packed statements. 
		#  |    char c  __attribute__((packed, aligned(2))); | So, struct-level alignment = max (1, 1, 2) = 2. Hence there is going to be 1-byte padding at the end.
		#  |  };                                             | Pedantic note: the packed attribute will be ignored for the char, since char is by definition packed.
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 16, because the compiler will calculate the struct-level alignment to be the 
		#  |    long long l __attribute__((packed,           | maximum of all individual member-level alignments. So, struct-level alignment = max (2, 2, 4) = 4. 
		#  |                               aligned(2)));     | This shows that aligned has the highest power. This is how the alignment of a member works.
		#  |    int i   __attribute__((packed, aligned(2))); |  First it is set to its natural alignment (say s).
		#  |    short s __attribute__((packed, aligned(4))); |  Then if there is a packed attribute, it is brought down to 1.
		#  |  };                                             |  Then if there if an aligned(m) attribute, that increases the alignment to m.
		#  |                                                 |  If there is no packed but only aligned, then it is set to max (s,m). Which basically means that
		#  |                                                 |  without a packed, aligned only works when it is bigger than the natural size. So, align only increases,
		#  |                                                 |  never reduces an alignment.
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 14, because the compiler will calculate the struct-level alignment to be the 
		#  |    long long l __attribute__((packed,           | maximum of all individual member-level alignments. So, struct-level alignment = max (2, 2, 2) = 2. 
		#  |                               aligned(2)));     | 
		#  |    int i   __attribute__((packed, aligned(2))); |  
		#  |    short s __attribute__((packed, aligned(2))); |  
		#  |  };                                             |  
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 16, because among all the alignment statements for c2, 8 wins.
		#  |      char c1;                                   | So, the only way c2 can be aligned to a 8-byte-boundary is if we add 7 bytes of pad after c1.
		#  |      char c2 __attribute__((aligned(2)))        |
		#  |              __attribute__((aligned(8)));       |
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 8, because among all the alignment statements for c1, 8 wins.
		#  |      char c1 __attribute__((aligned(2)))        | But, align(8) for a char means that after the compiler processes c1, it will allocate 8 bytes for c1.
		#  |              __attribute__((aligned(8)));       | Only the first byte will be actually used by c1, the rest 7 will be padding which will later be
		#  |      char c2;                                   | used by c2. 
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | #pragma pack(4)                                 | sizeof(B) = 8, because among all the alignment statements for c2, 8 wins, but that also gets reduced
		#  |  struct B {                                     | to 4 because of #pragma pack(4).
		#  |      char c1;                                   |
		#  |      char c2 __attribute__((aligned(2)))        |
		#  |              __attribute__((aligned(8)));       |
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | #pragma pack(4)                                 | sizeof(B) = 4, because among all the alignment statements for c1, 8 wins. But we also have the 
		#  |  struct B {                                     | #pragma pack(4) statement, which brings the alignment of c1 back to 4.
		#  |      char c1 __attribute__((aligned(2)))        | But, align(4) for a char means that after the compiler processes c1, it will allocate 1 bytes for c1
		#  |              __attribute__((aligned(8)));       | and 3 bytes of pads after it. This 3-byte-pad will then be utilized by c2.
		#  |      char c2;                                   | We do NOT mentally apply a aligned(4) for c2, since that will increase the alignment for c2.
		#  |  };                                             | #pragma pack(n) only decreases the alignment, never increases it.
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | #pragma pack(4)                                 | sizeof(B) = now 8.
		#  |  struct B {                                     | This example shows why #pragma pack(n) does not mean "apply align(n) to every member" automatically.
		#  |      char c1 __attribute__((aligned(2)))        | This is exactly the same as the previous example, but we have added the aligned(4) to c2 explicitly.
		#  |              __attribute__((aligned(8)));       | In the previously example, had #pragma pack(n) applied an "align(4)" to c2, it would be equivalent to this.
		#  |      char c2 __attribute__((aligned(4)));       | But now you see that by adding "aligned(4)" makes c2 also aligned to 4, which means it can no longer
		#  |  };                                             | utilize any part of those 3-byte padding after c1.
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  #pragma pack(2)                                | sizeof(B) = 14
		#  |  struct B {                                     | Each of these members get an alignment of 2. So that is the overall struct-level alignment.
		#  |    long long l;                                 | 
		#  |    int i;                                       | 
		#  |    short s;                                     | 
		#  |  };                                             | 
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 8, because the compiler will calculate the struct-level alignment to be the 
		#  |    int i   __attribute__((packed));             | maximum of all individual member-level alignments. Due to the __attribute__((packed)) statement,
		#  |    short s ;                                    | the alignment of int i is now 1. 
		#  |    char c;                                      | So, struct-level alignment = max (1, 2, 1) = 2. Hence there is going to be 1-byte padding at the end.
		#  |  };                                             | 
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 7, because the compiler will calculate the struct-level alignment to be the 
		#  |    int i   __attribute__((packed));             | maximum of all individual member-level alignments. Due to the __attribute__((packed)) statement,
		#  |    short s __attribute__((packed));             | the alignment of both int i and short s is now 1. 
		#  |    char c;                                      | So, struct-level alignment = max (1, 1, 1) = 1. Hence there is going to be no padding at the end.
		#  |  };                                             | 
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | 
		#  |    int i;                                       | sizeof(B) = 7, because when there is a packed statement at the struct-level, the compiler will calculate 
		#  |    short s ;                                    | the struct-level alignment to be 1, irrespective of all individual member-level alignments.
		#  |    char c;                                      |
		#  |  }__attribute__((packed));                      | 
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | This is the same as the previous example, except that we are starting with smaller items.
		#  |    char c;                                      | sizeof(B) = 7, because when there is a packed statement at the struct-level, the compiler will calculate 
		#  |    int i;                                       | the struct-level alignment to be 1, irrespective of all individual member-level alignments.
		#  |    short s ;                                    | Plus, that struct-level packed statement applies to all individual statements.
		#  |  }__attribute__((packed));                      | 
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 4, because when there is an aligned statement at the struct-level, that only applied to 
		#  |    char c1;                                     | the overall struct-level alignment - it does not apply to any individual member. This is different from
		#  |    char c2;                                     | the struct-level packed statement, which applies to all individual statements.
		#  |    char c3;                                     | Had the struct-level aligned(4) applied to all individual members, the sizeof(B) would have been 12.
		#  |  }__attribute__((aligned(4)));                  | 
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | #pragma pack(2)                                 | sizeof(B) = 10, because the compiler will pack i2 right after the short s.
		#  |  struct B {                                     | It's because 2 is smaller than sizeof(int), which is 4.
		#  |        int i1;                                  | 
		#  |        short s;                                 |
		#  |        int i2;                                  |
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | #pragma pack(4)                                 | sizeof(C) = 12, because now the compiler will pack int i2 from its natural alignement (4),
		#  |  struct C {                                     | 
		#  |        int i1;                                  | 
		#  |        short s;                                 |
		#  |        int i2;                                  |
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | #pragma pack(4)                                 | sizeof(D) = 12, because now the compiler will pack short s2 from its natural alignement (2),
		#  |  struct D {                                     | It's because 2 is smaller than 4 (the value in #pragma pack). Remember that #pragma pack(n) 
		#  |        int i1;                                  | can only reduce the overall alignment, never increase it.
		#  |        short s1;                                |
		#  |        short s2;                                |
		#  |        int i2;                                  |
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | #pragma pack(4)                                 | sizeof(E) = 12, because now the compiler will pack the double d from the packed-mandated 
		#  |  struct E {                                     | alignment of 4 rather than its natural alignement (8), It's because 4 is smaller than 8. 
		#  |        short s1;                                |
		#  |        double d;                                |
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | struct F1 {              |   struct F2 {        | sizeof(F1) = 1, and sizeof(F2) = 11. It's because the overall struct size will be aligned to the 
		#  |        char c;           |        char c[11];   | size of the largest element among the sturcture member variables, which is char here. 
		#  |  };                      |   };                 |
		#  |__________________________|______________________|____________________________________________________________________________________________________
		#  | #pragma pack(4)                                 | sizeof(G) = 1, despite the #pragma pack(4) directive. That's because #pragma pack() can only
		#  |  struct G {                                     | lower the alignment (than the natural alignment of any struct member variable. Since the member
		#  |        char c;                                  | variable here is a char, #pragma pack(n) for any value of n has no effect.
		#  |  };                                             |
		#  |_________________________________________________|____________________________________________________________________________________________________
		#  | struct H {                                      |sizeof(H) = 2. 
		#  |            short s;                             |
		#  |   };                                            |
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |                                                 | sizeof(I) = 8. That's because now the two aligned directives expands the short to 8 bytes and
		#  | struct I {                                      | 4 bytes, and irrespective of whichever aligned statement came first, the biggger one wins.
		#  |            short s __attribute__((aligned(8)))  | So, the following two declarations have the same effect:
		#  |                    __attribute__((aligned(4))); |  short s __attribute__((aligned(8)))  __attribute__((aligned(4)));
		#  |   };                                            |  short s __attribute__((aligned(4)))  __attribute__((aligned(8)));
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | #pragma pack(4)                                 | sizeof(J1) = 4. That's because now the two aligned directive expands the short to 8 bytes,
		#  | struct J1 {                                     | and the #pragma pack reduces it to 4. 
		#  |            short s __attribute__((aligned(4)))  | 
		#  |                    __attribute__((aligned(8))); |
		#  |   };                                            |
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | #pragma pack(8)                                 | sizeof(J2) = 4. That's because now the aligned directive expands the short to 4 bytes,
		#  | struct J2 {                                     | and the #pragma pack (8) cannot increase it because min(4,8) = 4.
		#  |            short s __attribute__((aligned(4))); | This shows the proof that #pragma pack does not mean that "Ignore the other aligned".
		#  |   };                                            | They are still processed.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | #pragma pack(1)                                 | sizeof(K) = now 2. That's because now the aligned directive expands the short to 4 bytes,
		#  |                                                 | in both size and alignment, but and the #pragma pack(1) reduces the size to 2.
		#  | struct K {                                      | It cannot reduce the size to 1 because a short takes 2 bytes at the minimum. However, the other part 
		#  |            short s __attribute__((aligned(4))); | of a #pragma pack(n) statement is the "packing" part, which we will see in the next example.
		#  |   };                                            | So, after the aligned(4) expanded the size and alignment for the short to 4 from 2, 
		#  |                                                 | the pragma pack(1) reduces the size from 4 to 2, and the alignment from 4 to 1.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | #pragma pack(1)                                 | sizeof(L) = now 3. That's because now the aligned directive expands the short to 4 bytes in size and alignment,
		#  | struct L {                                      | and the #pragma pack(1) reduces the size back to 2. It cannot reduce the size to 1 because a short takes
		#  |            char c;                              | 2 bytes at the minimum. However, the other part of a #pragma pack(n) statement is the
		#  |            short s __attribute__((aligned(4))); | "packing" part, which allows the short s to map from the second byte iteself.
		#  |   };                                            | Also, observe that now the short s is aligned to a 1-byte boundary, overriding its natural 2-byte size.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |                                                 | This is exactly the same as the previous one, exept the #pragma pack(1) part. Now, we will see
		#  | struct M {                                      | sizeof(M) = now 8. That's because now the aligned directive expands the short to 4 bytes,
		#  |            char c;                              | and without the #pragma pack(1) statement there is nothing to reduce it.
		#  |            short s __attribute__((aligned(4))); | And now this 4-byte short can only be aligned at a 4-byte boundary.
		#  |   };                                            | There is no "packing" part, which allows the short s to map from the second byte iteself.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |                                                 | This is exactly the same as the previous one, exact the  __attribute__((packed)) part. Now, we will see
		#  | struct __attribute__((packed)) N1 {             | sizeof(N1) = still 8. That's because now the aligned directive expands the short to 4 bytes,
		#  |            char c;                              | and without the #pragma pack(1) statement there is nothing to reduce it.
		#  |            short s __attribute__((aligned(4))); | And now this 4-byte short can only be aligned at a 4-byte boundary.
		#  |   };                                            | There is no packing "packing" part, which allows the short s to map from the second byte iteself.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | #pragma pack(1)                                 | This is exactly the same as the previous one, exact the  #pragma pack(1). Now, we will see
		#  | struct __attribute__((packed)) N2 {             | sizeof(N2) = now 3. That's because now the aligned directive expands the short to 4 bytes,
		#  |            char c;                              | but the #pragma pack(1) statement reduces it back to 2 bytes. Also, the #pragma pack(1) overrides the requirement
		#  |            short s __attribute__((aligned(4))); | for the aligned(4) that the short can only be aligned at a 4-byte boundary.
		#  |   };                                            | So it starts packing from the second byte itself.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#
		#
		######################################################################################################################################
		# Rules of Bitfields 
		######################################################################################################################################
		#
		#  A bitfield statement is like char c1 : 7; They can be signed or unsigned. There can be __attribute__(()) statements like packed or aligned().
		#  The container (datatype) for a bitfield is the integer type - char / short / int / long / long long etc.
		#  In a bitfield sequence, we can have a mixture of datatypes. For example, this following is a valid struct:
		#
		#  struct mixed {                      _
		#					char c: 7;			\
		#					short s: 14;         |
		#					long long ll: 63;     >  bitfield sequence # 1
		#					char c2: 1;        _/ 
		#
		#					int i;
		#                                      _
		#					char c2: 7;			\
		#					short s2: 14;        |
		#					int i1: 3;            >  bitfield sequence # 2
		#					int i2: 20;          |
		#					char c3: 1;        _/ 
		#				};
		#
		
		
		
		
		
		
		
		
		

		#  ===================================   This part below needs to be deleted once we implement it correctly ==============================
		#
		# It is highly compiler-dependent. There is no guarantee it will match with the actual implementations.
		#
		# 1. Bitfields cannot cross their container boundaries - it will just add padding. Which means, the situation below will result in 12 bytes (3 ints), not 8 (2 ints)
		#      int a:31, b:2, c:31;
		#
		# 2. Size of structs containing Bitfields CAN have odd values, like 1,3,5,7,9 etc.
		#
		# 3. Total Bitfield size will depend on the maximum-sized container within the list, if it is mixed type. If all the types are identical, there is no choosing (makes life easy).
		#    For example, int i:28; char c: 7; will get a size of two ints (8 bytes). Yet, char c1: 7, c2: 7, c3: 7, c4: 7; char c5: 7; will get a size of 5 bytes.
		#    This is because in the latter case the maximum-sized container is a char, while in the former it is an int.
		#
		#    Also, <char b3:2; int i: 28; short s: 3;> will require 2 ints (8 bytes) where <char b3:2; int i: 27; short s: 3;> would only require 1 int (4 bytes).
		#
		#    Only one exception: If there is a long long (whose size is 8 bytes), we still seem to be using the multiple of 4 bytes only after 8.
		#    So,  <char b3:7; long long int i: 58;> would require 12 bytes (not 16) while <char b3:6; long long int i: 58;> would only require 8.
		#
		#  This can lead to a paradoxical situation where by supplying a BIGGER container, one can REDUCE the overall size. But that is really not paradoxical,
		#  because a bigger container can allow better packing, while for a smaller container one would waste more empty space.
		# 
		#    <short a:9, b:9, c:9; > would take 6 bytes. But <int a:9, b:9, c:9; > would take only 4 bytes. 
		#
		#  Therefore, whenever you get a sequence of bitfields in a struct definition (recall that a single struct can have multiple disjoint bitfield sequences, 
		#  this the way to figure out the size of that sequence:
		# 
		#   a. Suppose the structure has 3 members, with 3 different containers X, Y and Z. Go through the sequence to find out the largest container out of X, Y and Z(say it is Y).
		#   b. For each member, ignore the respective container. For example, if the first member's container size is X but size(X) < size(Y), ignore X. Assume every container is Y.
		#   c. Start packing items one by one into an Y container. The moment adding another item would exceed the container, start another Y container.
		#   d. For Big-endian, pack from MSb to LSb (where the MSb can be at the max 63). For Little-endian, pack from LSb to MSb.

		#  ===================================   This part above needs to be deleted once we implement it correctly ==============================
		#
		
		
		#
		#  Some examples of bitfields with aligned, packed and #pragma pack (the used bits are marked as 1, the pads are 0, MSb on the left, LSb on the right):
		#
		#	Main rule:
		#	
		#	1. Usually, look at the current first unfilled bit. From there, go back to the closest past address that will support the alignment of the current datatype.
		#      For example, if it is a char, it will be aligned to a byte. For short, 2-bytes. For int, 4 bytes etc.
		#
		#   2. Check if there is an __aligned__ attribute at the member-level. If there is, irrespective of whether this member is packed or not, aligned would prevail.
		#      That aligned(m) may potentially be reduced by a #pragma pack(n), but in no case will it fall below the 1-byte boundary. And this works even if the
		#      m in aligned(m) is less than the naturnal size of the variable (for example, a "short s:5 __attribute__((aligned(1)));" statement.
		#
		#      You might be wondering - wait, for non-bitfields, aligned(m) always INCREASES the alignment - it never reduces. That's why, if we have a statement
		#      like "int i __attribute__((aligned(2)));", the aligned(2) is ignored since its aligned value (2) is less than the current alignment (4). Of course,
		#      if there were a __attribute__ ((packed)) too, then it were a different matter since the packed would first bring down the alignment to 1 byte, which
		# 	   the __attribute__((aligned(2))) will then INCREASE to 2. But, without any such packed thing here, how does the aligned(m) in statements like
		#	   "short s:5 __attribute__((aligned(1)));" still work? Aren't they reducing rather than increasing?
		#
		#	   The answer is - an aligned(m) always increases the alignment, never reduces. When you think in terms of bitfields, even without a packed statement,
		#      a bitfield occupies the very next bit (a packed statement makes a single  bitfiled to potentially overlap two different containers, if required).
		#      This means that current alignment is 1 BIT. When there is an aligned(1) statement, that means we are expanding the bit-packing-alignment to 1 BYTE.
		#      That's a increase from 1 BIT to 1 BYTE, which is an eight-fold increase.
		#
		#      In essense, the rules for determining the first eligible bit for loading the current bitfield member is:
		#		- No aligned(m): First unfilled bit (bit #c) as the possible packing place.
		#		- There are member-level aligned(m) attributes. Find out the overall alignment (which will be aligned to some 2's power of bytes). The first bit
		#		  adhering to this alignment is first eligible bit.
		#      
		#	   But, remember that just because we find this first "eligible" bit does not mean we will be able to pack the current member here - it depends on
		#      how big (number of bits) the current bitfield member is, and how many bits are left in the current container.
		#
		#   3. See if the remaining unfilled bits will be able to fully accommodate the current bits. If yes, fill it. 
		#      If not, then you need to check if it is packed.
		#      A struct can be packed by either at the packed attribute at the member-level, at the struct-level, or by a #pragma pack(n) statement.
		#      - If the member is not "packed", then go to the next address that supports the current alignment.
		#        For that, you need to look at the natural size(s), aligned(m), packed, and #pragma pack(n). Use the same ruleset as non-bitfield.
		#      - If it is packed, start packing from the current bit.
		#   
		#   4. The overall alignment of the structure follows the same rule - max of the individual alignments of each member. However,
		#
		#	We use these notations in the examples below:
		#	   	m - the power of 2 (1/2/4/8) in any __attribute__((aligned(m))) statement, if one exists
		#	   	n - the power of 2 (1/2/4/8) in any #pragma pack(n) statement, if one exists
		#		s - natural size for a data type (1 for char, 2 for short, 4 for int/long, 8 for long long etc.)
		#		a - final alignment for a struct member, after considering all the s, m and n. The overall struct is a multiple of this
		#		b - the number of bits sought for the current bitfield, must have b <= s (no, even if a > s, we still cannot have s < b < a)
		#	        So, this is illegal ==> 	short s:17 __attribute__((aligned(4)));
		#      		It does not matter that we have increased the alignment to 32 bits - if we are using short, we cannot use b > 16.
		#		c - the cumulative number of bits that have already been filled (including pads) up to now. Also represents the bit# for the first available bit to pack.
		#
		#
		#      This essentially means that, if a < s (like aligned(1) for a short or aligned(1/2) for an int), 
		#	   then you can start packing within the current container but at the a-byte alignment. So, find the first a-byte-aligned bit after the first c bits.
		#		- short s: b __attribute__((aligned(1))); 	<== Here the s can start packing from the bit #8 of the current short container. 
		#		  If b <= 8, then it can be accommodated in the byte1. Else, start from Byte2.
		#		- int i: b __attribute__((aligned(1))); 	<== Here the s can start packing from the second LSbyte of the current short container. 
		#	   On the other hand, for the ultimate alignment of m and natural container size (s), if m < s (like aligned(1) for a short or aligned(1/2) for an int), 
		#   _____________________________________________________________________________________________________________________________________________________
		#  |  struct A {                                     | sizeof(A) = 2, because now the compiler will pack int i2 right after i1.
		#  |        short i1:5;                              | So there will be a pad of 4 bits after i2.
		#  |        short i2:7;                              | i1 = 00000000 00011111 
		#  |  };                                             | i2 = 00001111 11100000
		#  |                                                 | ALL  00001111 11111111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct A {                                     | sizeof(A) = 2, because now the compiler will pack int i2 right after i1.
		#  |        short i1:5;                              | So there will be a pad of 4 bits after i2.
		#  |        short i2:7 __attribute__((packed));      | i1 = 00000000 00011111 
		#  |  };                                             | i2 = 00001111 11100000
		#  |  // The __attribute__((packed)) is redundant    | ALL  00001111 11111111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct A {                                    | sizeof(A) = now 2, because without the packed, now it is aligned to its "utilized" size (2 bytes).
		#  |        short i1:5;                              |       byte1    byte0  
		#  |        short i2:7 __attribute__((aligned(1)));  | i1 = 00000000 00011111
		#  |  };                                             | i2 = 01111111 00000000
		#  |                                                 | ALL  01111111 00011111
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct __attribute__((packed)) A {            | sizeof(A) = still 2, irrespective of the fact that there is a struct-level packed.
		#  |												 | Shows that the moment we have aligned(), you can never pack at the bit-level - you start at a new byte.
		#  |        char i1:1 __attribute__((packed));       | Here we went overboard with putting packed statement everywhere, but it did not matter.
		#  |                                                 |       byte1    byte0  
		#  |        char i2:1 __attribute__((packed,         | i1 = 00000000 00000001
		#  |  };                    aligned(1)));            | i2 = 00000001 00000000
		#  |                                                 | ALL  00000001 00000001
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | // No pragma pack                               | sizeof(A) = 2.
		#  |  struct A {                                     |       byte1    byte0  
		#  |     short i1: 1;                                |i1 = 00000000 00000001
		#  |   };                                            |
		#  |                                                 |
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | #pragma pack(1)                                 | sizeof(A) = 1.
		#  |  struct A {                                     |        byte0  
		#  |     short i1: 1;                                | i1 = 00000001
		#  |   };                                            | Observe that even in absense of any __aligned__ attribute, the #pragma pack(1) was still able to 
		#  |                                                 | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | // No pragma pack                               | sizeof(A) = 4.
		#  |  struct A {                                     |       byte3    byte2    byte1    byte0  
		#  |     int i1: 1;                                  |i1 = 00000000 00000000 00000000 00000001
		#  |   };                                            |
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | // No pragma pack                               | sizeof(A) = still 4. The aligned(2) is ignored since align can only increase, not reduce alignment.
		#  |  struct A {                                     |       byte3    byte2    byte1    byte0  
		#  |     int i1: 1 __attribute__((aligned(2)));      |i1 = 00000000 00000000 00000000 00000001
		#  |   };                                            | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | // No pragma pack                               | sizeof(A) = now 2. The aligned(2) now works since align can now increase the post-packed alignment of 1
		#  |  struct A {                                     |       byte1    byte0  
		#  |     int i1: 1 __attribute__((aligned(2)))       |i1 = 00000000 00000001
		#  |               __attribute__((packed));          |
		#  |   };                                            | 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | // No packed, or pragma pack                    | sizeof(A) = 4. Since a short can only hold 16 bits, we start from a new short boundary.
		#  |  struct A {                                     |        byte3    byte2    byte1    byte0  
		#  |     short i1: 15;                               | i1 = 00000000 00000000 01111111 11111111 
		#  |     short i2: 2;                                | i2 = 00000000 00000011 00000000 00000000 
		#  |  };                                             | ALL  00000000 00000011 01111111 11111111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | // No pragma pack, but there is a packed        | sizeof(A) = still 4. But, we are NOT starting from the new short boundary - i2 overlaps both shorts.
		#  |  struct A {                                     |        byte3    byte2    byte1    byte0  
		#  |     short i1: 15;                               | i1 = 00000000 00000000 01111111 11111111 
		#  |     short i2: 2 __attribute__((packed));        | i2 = 00000000 00000001 10000000 00000000 
		#  |  };                                             | ALL  00000000 00000001 11111111 11111111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | #pragma pack(2), but no packed                  | sizeof(A) = still 4. But, we are NOT starting from the new short boundary - i2 overlaps both shorts.
		#  |  struct A {                                     |        byte3    byte2    byte1    byte0  
		#  |     short i1: 15;                               | i1 = 00000000 00000000 01111111 11111111 
		#  |     short i2: 2;                                | i2 = 00000000 00000001 10000000 00000000 
		#  |  };                                             | ALL  00000000 00000001 11111111 11111111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  | #pragma pack(1)                                 | sizeof(A) = 3. Bits are packed in the same packed fashion, but the overall alignment is 1 byte.
		#  |  struct A {                                     |        byte2    byte1    byte0  
		#  |     short i1: 15;                               | i1 = 00000000 01111111 11111111 
		#  |     short i2: 2;                                | i2 = 00000001 10000000 00000000 
		#  |  };                                             | ALL  00000001 11111111 11111111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct A {                                     | sizeof(A) = 4, because now i2 is aligned to a 2-byte boudary. So there will be a pad of 4 bits after i2.
		#  |        short i1:5;                              | Observe that 5+7 bits = 12 bits fit into a single short, yet i2 starts from a new short boundary.
		#  |                                                 |       byte3    byte2    byte1    byte0  
		#  |        short i2:7 __attribute__((aligned(2)));  | i1 = 00000000 00000000 00000000 00011111  
		#  |  };                                             | i2 = 00000000 01111111 00000000 00000000 
		#  |                                                 | ALL  00000000 01111111 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct A {                                     | sizeof(A) = still 4, because now i2 is aligned to a 2-byte boudary. So there will be a pad of 4 bits after i2.
		#  |        short i1:5;                              | Observe that 5+7 bits = 12 bits fit into a single short, yet i2 starts from a new short boundary.
		#  |                                                 |       byte3    byte2    byte1    byte0  
		#  |        short i2:7 __attribute__((aligned(2)));  | i1 = 00000000 00000000 00000000 00011111  
		#  |  } __attribute__((packed)) ;                    | i2 = 00000000 01111111 00000000 00000000 
		#  |                                                 | ALL  00000000 01111111 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct B {                                     | sizeof(B) = 2, because now the compiler will pack int i2 right after i1.
		#  |        short i1:5;                              | So there will be a pad of 2 bits after i2. 
		#  |        short i2:9;                              | i1 = 00000000 00011111 
		#  |  };                                             | i2 = 00111111 11100000
		#  |                                                 | ALL  00111111 11111111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  __attribute__((packed)) struct B {             | sizeof(B) = 2, because now the compiler will pack int i2 right after i1.
		#  |        short i1:5;                              | So there will be a pad of 2 bits after i2. The __attribute__((packed)) is redundant here (no aligned).
		#  |        short i2:9;                              | i1 = 00000000 00011111 
		#  |  };                                             | i2 = 00111111 11100000
		#  |  // packed is redundant                         | ALL  00111111 11111111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct C {                                     | sizeof(C) = 4, because i2 will now be aligned to a 2-byte boundary.
		#  |        short i1:5;                              |       byte3    byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(2)));  | i1 = 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000001 11111111 00000000 00000000 
		#  |                                                 | ALL  00000001 11111111 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  __attribute__((packed)) struct C {             | sizeof(C) = still 4, because aligned has more power than packed.
		#  |        short i1:5;                              |       byte3    byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(2)));  | i1 = 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000001 11111111 00000000 00000000 
		#  |                                                 | ALL  00000001 11111111 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = now 4, because without the packed, now it is aligned to i1's size (2 bytes).
		#  |        short i1:5;                              |       byte3    byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(1)));  | i1 = 00000000 00000000 00000000 00011111  
		#  |  };                                             | i2 = 00000001 11111111 00000000 00000000 
		#  |                                                 | ALL  00000001 11111111 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = still 4, because without the packed for i1, it's still aligned to max-sized i1's size (2 bytes).
		#  |        short i1:5 __attribute__((aligned(1)));  |       byte3    byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(1)))   | i1 = 00000000 00000000 00000000 00011111 
		#  |                   __attribute__((packed));      | i2 = 00000001 11111111 00000000 00000000 
		#  |  };                                             | ALL  00000001 11111111 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = now 3, because now the max-sized alignment is 1 byte. We have packed on each struct member level,
		#  |        short i1:5 __attribute__((aligned(1)))   | which is same as putting a packed in the struct-level, as the example below
		#  |                   __attribute__((packed));      |       byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(1)))   | i1 = 00000000 00000000 00011111 
		#  |                   __attribute__((packed));      | i2 = 00000001 11111111 00000000 
		#  |  };                                             | ALL  00000001 11111111 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  __attribute__((packed)) struct C {             | sizeof(C) = now 3, because now it is byte-aligned.
		#  |        short i1:5;                              |       byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(1)));  | i1 = 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000001 11111111 00000000 
		#  |                                                 | ALL  00000001 11111111 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  #pragma pack(2)                                | sizeof(C) = 4, because now it is byte-aligned.
		#  |   struct C {                                    |
		#  |        short i1:5;  // aligned(1) is redundant  |       byte3    byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(1)));  | i1 = 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000000 00000001 11111111 00000000 
		#  |                                                 | ALL  00000000 00000001 11111111 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = still 4, but look at the placement of i2. It's no longer at byte #2, it's now at byte#1
		#  |        short i1:5;                              |       byte3    byte2    byte1    byte0  
		#  |        int   i2:9 __attribute__((aligned(1)));  | i1 = 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000000 00000001 11111111 00000000 
		#  |                                                 | ALL  00000000 00000001 11111111 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = still 4, because you can still start at a byte-aligned second byte, and fill it within 1 int.
		#  |        short i1:5;                              |       byte3    byte2    byte1    byte0  
		#  |        int   i2:24 __attribute__((aligned(1))); | i1 = 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 11111111 11111111 11111111 00000000 
		#  |                                                 | ALL  11111111 11111111 11111111 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = still 4, because you can still start at a byte-aligned second byte, and fill it within 1 int.
		#  |        short i1:5;                              |       byte3    byte2    byte1    byte0  
		#  |        int   i2:24 __attribute__((aligned(1))); | i1 = 00000000 00000000 00000000 00011111 
		#  |  } __attribute__((packed));                     | i2 = 11111111 11111111 11111111 00000000 
		#  |  // packed is redundant                         | ALL  11111111 11111111 11111111 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = 8, because when you start packing from the byte2, you cannot fit in 24 bits witin the next 2 bytes.
		#  |                                                 | So you go to the next place where the int container can start (byte4) and pack from there.
		#  |        short i1:5;                              |        byte7    byte6    byte5    byte4   byte3    byte2    byte1    byte0  
		#  |        int   i2:24 __attribute__((aligned(2))); | i1 = 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000000 11111111 11111111 11111111 00000000 00000000 00000000 00000000 
		#  |                                                 | ALL  00000000 11111111 11111111 11111111 00000000 00000000 00000000 00011111 
		#  |                                                 | Because we did not have a packed attribute, aligned(2) was not able to REDUCE the alignemnt of where the 
		#  |                                                 | next int container could start from. Its alignment remained it natural size, 4.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = 6, because when you start packing from the byte2, you cannot fit in 24 bits witin the next 2 bytes.
		#  |                                                 | So you go to the next place where the int container can start (byte2) and pack from there.
		#  |        short i1:5;                              |        byte5    byte4   byte3    byte2    byte1    byte0  
		#  |        int   i2:24 __attribute__((aligned(2)))  | i1 = 00000000 00000000 00000000 00000000 00000000 00011111 
		#  |                    __attribute__((packed));     | i2 = 00000000 11111111 11111111 11111111 00000000 00000000 
		#  |  };                                             | ALL  00000000 11111111 11111111 11111111 00000000 00011111 
		#  |                                                 | Because we have a packed attribute, it initially reduced the the alignemnt to 1 of where the next int container
		#  |                                                 | could start from. Then aligned(2) INCREASED that alignment to 2.
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = still 4, No change due to the int -> long long shift
		#  |      short i1:5;                                |       byte3    byte2    byte1    byte0  
		#  |      long long i2:9 __attribute__((aligned(1)));| i1 = 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000000 00000001 11111111 00000000 
		#  |                                                 | ALL  00000000 00000001 11111111 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = still 4, No change due to the int -> long long shift
		#  |      short i1:5;                                |       byte3    byte2    byte1    byte0  
		#  |      long long i2:9 __attribute__((aligned(2)));| i1 = 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000001 11111111 00000000 00000000
		#  |                                                 | ALL  00000001 11111111 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |   struct C {                                    | sizeof(C) = now 8, No change due to the int -> long long shift ???????????????????????????????????
		#  |      short i1:5;                                |       byte3    byte2    byte1    byte0  
		#  |      long long i2:9 __attribute__((aligned(4)));| i1 = 00000000 00000000 00000000 00011111 is this correct?
		#  |  };                                             | i2 = 00000001 11111111 00000000 00000000
		#  |                                                 | ALL  00000001 11111111 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  struct D {                                     | sizeof(D) = 8, because i2 will now be aligned to a 4-byte boundary.
		#  |        short i1:5;                              |       byte7    byte6    byte5    byte4   byte3    byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(4)));  | i1 = 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000000 00000000 00000001 11111111 00000000 00000000 00000000 00000000 
		#  |                                                 | ALL  00000000 00000000 00000001 11111111 00000000 00000000 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  __attribute__((packed)) struct E {             | sizeof(E) = still 8, because __attribute__ aligned has more power than packed.
		#  |        short i1:5;                              |       byte7    byte6    byte5    byte4   byte3    byte2    byte1    byte0  
		#  |        short i2:9 __attribute__((aligned(4)));  | i1 = 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00011111 
		#  |  };                                             | i2 = 00000000 00000000 00000001 11111111 00000000 00000000 00000000 00000000 
		#  |                                                 | ALL  00000000 00000000 00000001 11111111 00000000 00000000 00000000 00011111 
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  #pragma pack(2)                                | sizeof(F) = 4, because even though aligned brings up the alignement to 4, the #pragma pack brings it
		#  |  struct F {                                     | down to 2.
		#  |                                                 |       byte3    byte2    byte1    byte0  
		#  |        short i1:5;                              | i1 = 00000000 00000000 00000000 00011111
		#  |        short i2:9 __attribute__((aligned(4)));  | i2 = 00000001 11111111 00000000 00000000
		#  |  };                                             | ALL  00000001 11111111 00000000 00011111
		#  |_________________________________________________|_____________________________________________________________________________________________________
		#  |  #pragma pack(1)                                | sizeof(F) = 3, because even though aligned brings up the alignement to 4, the #pragma pack brings it
		#  |  struct F {                                     | down to 1.
		#  |        short i1:5;                              | i1 = 00000000 00000000 00011111 
		#  |        short i2:9 __attribute__((aligned(4)));  | i2 = 00000001 11111111 00000000 
		#  |  };                                             | ALL  00000001 11111111 00011111
		#  |_________________________________________________|_____________________________________________________________________________________________________
		
		# By this time all the individual members of the struct/union have been evaluated (including bitfields), hence we can calculate the overall length of the structure 
		PRINT ("INFO: The structuresAndUnionsDictionary[",structName,"] = ",structuresAndUnionsDictionary[structName] )
		PRINT ("Its structuresAndUnionsDictionary[structName][\"components\"] has ",len(structuresAndUnionsDictionary[structName]["components"]),"members")
		
		# When dealing with bitfields, this figure is inclusive of the last potentially partially filled byte too.
		# For example, if we have 3 bitfields struct { char c1:4; char c2:4; char c3:4; }; then structSizeBytes = 2, even though the last byte is only partially filled.
		structSizeBytes = 0		
		
										# 
		
		currentCumulativeBitfieldSizeInBits = 0
		bitFieldComponentListBeginIndex = None
		bitFieldComponentListEndIndex = None
		
		largestContainerYet = 0
		
		structComponentList = structuresAndUnionsDictionary[structName]["components"]
		
		# This list will be converted into a dictionary later and only the dictionary (bitFieldInfo) then will be plugged back into the 
		# structuresAndUnionsDictionary[structName]["components"]. So, this list is just an scratchpad variable here.
		
		# Technically, we can declare a struct with some of its component being bitfields and some non-bitfields. 
		# We can mix and match - C does not mandate that all the bitfield components must come contiguously.
		# For example, this is a valid struct declaration:
		#
		# struct weird { 
		#				 float f; 
		#				 int i1; 
		#				 int i2:3;   <== bitfield
		#				 int i3; 
		#				 int i4:10;  <== bitfield
		#				 short s:5;	 <== bitfield
		#				 int i6;
		#				};
		#
		structMemberIsBitfield = []	# For every struct member, we just fill it up with True/False depending on if it is a bitField or not. Also do some basic sanity checking.
		
		for N in range(len(structComponentList)):
			structMemberDescription = structComponentList[N][4]
			structMemberBaseTypeSize = structComponentList[N][1]
			if structMemberDescription["isBitField"] not in (True, False):
				errorMessage = "structMemberDescription[\"isBitField\"] must be either True or False; current value is : " + STR(structMemberDescription["isBitField"])
				errorRoutine(errorMessage)
				return False
			elif structMemberDescription["isBitField"] == True and "bitFieldWidth" not in getDictKeyList(structMemberDescription):
				errorMessage = "structMemberDescription[\"bitFieldWidth\"] must be present for a bit array"
				errorRoutine(errorMessage)
				return False
			elif structMemberDescription["isBitField"] == True and not (0 <= structMemberDescription["bitFieldWidth"] <= structMemberBaseTypeSize*BITS_IN_BYTE):
				errorMessage = "ERROR: Invalue value of structMemberDescription[\"bitFieldWidth\"] - "+STR(structMemberDescription["bitFieldWidth"])
				errorRoutine(errorMessage)
				return False
			elif structMemberDescription["isBitField"] == True:
				structMemberIsBitfield.append([True,structMemberDescription["baseType"],structMemberDescription["bitFieldWidth"]])
			else:
				structMemberIsBitfield.append(False)
				
		if 	len(structMemberIsBitfield) != len(structComponentList):
			errorMessage = "ERROR in coding: len(structMemberIsBitfield) = %d != len(structuresAndUnionsDictionary[structName][\"components\"] =%d "%(len(structMemberIsBitfield), len(structuresAndUnionsDictionary[structName]["components"]))
			errorRoutine(errorMessage)
			return False

		# It should print something like [True, basetype, bitfieldwidth]
		#   {
		#	 False,
		#	 False,
		#	 [True, int,3],
		#	 False,
		#	 [True, int,10],
		#	 [True, short,5],
		#	 False
		#	]
		PRINT ("structMemberIsBitfield =",structMemberIsBitfield)
		

		bitFieldSequences =[]	# Each member should be of form [startIndex, stopIndex]
		
		# Calculate the different sequences in the struct memberlist
		structComponentListBitFieldSequenceBeginIndex = None
		structComponentListBitFieldSequenceEndIndex = None
		N = 0
		while (N<len(structMemberIsBitfield)):
			# If this component is not a bitfield, we just use False. But, if it is a bitfield, we have a list there instead with first member being True. So, don't check for True.
			if structMemberIsBitfield[N] != False: 	
#				if N == 0 or (N>0 and (structMemberIsBitfield[N-1] == False or (structMemberIsBitfield[N-1][2]==0))):
				if N == 0 or (N>0 and (structMemberIsBitfield[N-1] == False )):
					structComponentListBitFieldSequenceBeginIndex = N
#				if N == len(structMemberIsBitfield)-1 or (N<len(structMemberIsBitfield)-1  and (structMemberIsBitfield[N+1] == False or structMemberIsBitfield[N+1][2]==0)):
				if N == len(structMemberIsBitfield)-1 or (N<len(structMemberIsBitfield)-1  and (structMemberIsBitfield[N+1] == False )):
					structComponentListBitFieldSequenceEndIndex = N
					if structComponentListBitFieldSequenceBeginIndex == None or structComponentListBitFieldSequenceBeginIndex > structComponentListBitFieldSequenceEndIndex:
						errorMessage = "ERROR in coding: structComponentListBitFieldSequenceBeginIndex (%d) > structComponentListBitFieldSequenceEndIndex (%d) "%(structComponentListBitFieldSequenceBeginIndex,structComponentListBitFieldSequenceEndIndex)
						errorRoutine(errorMessage)
						return False
					else:
						for t in range(structComponentListBitFieldSequenceBeginIndex, structComponentListBitFieldSequenceEndIndex+1):
							if structMemberIsBitfield[t] == False:
								errorMessage = "ERROR in coding: For bitfield sequence <structComponentListBitFieldSequenceBeginIndex (%d), structComponentListBitFieldSequenceEndIndex (%d)>, item=%d is not a bitfield"%(structComponentListBitFieldSequenceBeginIndex,structComponentListBitFieldSequenceEndIndex,t)
								errorRoutine(errorMessage)
								return False
					# At this point, we are assuming that the bitfield sequence is correct		
					bitFieldSequences.append([structComponentListBitFieldSequenceBeginIndex,structComponentListBitFieldSequenceEndIndex])
					structComponentListBitFieldSequenceBeginIndex = None
					structComponentListBitFieldSequenceEndIndex = None
			N += 1

		# For the above example, it will print something like
		#  bitFieldSequences = [
		#						[2,2],		<== The first bitfield sequence (int container)
		#						[4,5]		<== The second bitfield sequence (a mix of int and short containers)
		#						]
		#
		PRINT ( "bitFieldSequences =",bitFieldSequences)

		# Now, just because we have a bitfield sequence does not necessarily mean that ALL the containers within that sequence will be the same.
		if bitFieldSequences:
			bitSequenceCount = 0
			while bitSequenceCount<len(bitFieldSequences):
				structComponentListBitFieldSequenceBeginIndex = bitFieldSequences[bitSequenceCount][0]
				structComponentListBitFieldSequenceEndIndex	  = bitFieldSequences[bitSequenceCount][1]
				largestContainer = None
				largestContainerSizeInBytes = 0	
				for t in range(structComponentListBitFieldSequenceBeginIndex,structComponentListBitFieldSequenceEndIndex+1):
					currentContainerSizeInBytes = structComponentList[t][1]	
					# For long long, we are putting a override.
#					currentContainerSizeInBytes = 4 if structComponentList[t][1]==8 else currentContainerSizeInBytes	# Long Long still aligns to word boundary
					if currentContainerSizeInBytes > largestContainerSizeInBytes:
						largestContainerSizeInBytes = currentContainerSizeInBytes
						largestContainerDatatype = structComponentList[t][4]["datatype"]
				PRINT ("For bitSequenceCount =%d (<%d,%d>), the largestContainerDatatype = %s and largestContainerSizeInBytes = %d"%(bitSequenceCount,structComponentListBitFieldSequenceBeginIndex,structComponentListBitFieldSequenceEndIndex,largestContainerDatatype,largestContainerSizeInBytes))
				for t in range(structComponentListBitFieldSequenceBeginIndex,structComponentListBitFieldSequenceEndIndex+1):
					structMemberIsBitfield[t].append(bitFieldSequences[bitSequenceCount])
					structMemberIsBitfield[t].append([largestContainerDatatype, largestContainerSizeInBytes])
				bitSequenceCount += 1
		
		# It should print something like [True, basetype, bitfieldwidth,[bitFieldSequenceStartComponent#,bitFieldSequenceEndComponent#],[largestContainerDatatype, largestContainerSizeInBytes]]
		#   {
		#	 False,
		#	 False,
		#	 [True, int,3,[2,2],[int,4]],
		#	 False,
		#	 [True, int,10,[4,5],[int,4]],
		#	 [True, short,5,[4,5],[int,4]],
		#	 False
		#	]
		PRINT ("\n"*3,"After updating the bitSequence information and largestContainerSizeInBytes for each bitfield sequence, structMemberIsBitfield =")
		PRINT ("==="*50)
		for item in structMemberIsBitfield:
			PRINT (item)
		PRINT ("==="*50)
		PRINT("\n"*3)

		# Now we are actually going to start packing it
		containerNumber = 0		# How many containers we need to display all these data
		N = 0
		while (N<len(structMemberIsBitfield)):
			if structMemberIsBitfield[N] == False: 	# Don't use True, we have a list there instead
				containerNumber = 0		# How many containers we need to display all these data. We reset this counter every time we hit a non-bitfield item
			elif structMemberIsBitfield[N] != False: 	# Don't use True, we have a list there instead
				containerSizeInBits = structMemberIsBitfield[N][4][1]*BITS_IN_BYTE
				fieldSizeInBits = structMemberIsBitfield[N][2]
				if not (structMemberIsBitfield[N][3][0] <= N <= structMemberIsBitfield[N][3][1]):
					errorMessage = "ERROR in coding: current struct component # N=%d is outside bitfield sequence <structComponentListBitFieldSequenceBeginIndex (%d), structComponentListBitFieldSequenceEndIndex (%d)>, item=%d is not a bitfield"%(N,structComponentListBitFieldSequenceBeginIndex,structComponentListBitFieldSequenceEndIndex)
					errorRoutine(errorMessage)
					return False
				elif fieldSizeInBits > containerSizeInBits:	# Should be caught earlier
					errorMessage = "ERROR in coding: current struct component # N=%d within bitfield sequence <structComponentListBitFieldSequenceBeginIndex (%d), structComponentListBitFieldSequenceEndIndex (%d)>, item=%s has fieldSizeInBits (%d) > containerSizeInBits (%d)"%(N,structComponentListBitFieldSequenceBeginIndex,structComponentListBitFieldSequenceEndIndex,STR(structMemberIsBitfield[N]), fieldSizeInBits, containerSizeInBits)
					errorRoutine(errorMessage)
					return False

				# TO-DO: We need to handle the case where the first one or more items in the sequence have zero-width bitfield
				if N == structMemberIsBitfield[N][3][0]:	# first item in the sequence, which is the fourth item in structMemberIsBitfield
					bitStart = 0
					bitEndInclusive = fieldSizeInBits-1		# inclusive
					bitsLeft = containerSizeInBits - fieldSizeInBits
				else:
					if fieldSizeInBits == 0:
						containerNumber += 1
						bitStart = 0
						bitEndInclusive = fieldSizeInBits-1	# inclusive
						bitsLeft = containerSizeInBits - fieldSizeInBits
					elif fieldSizeInBits > bitsLeft:
						containerNumber += 1
						bitStart = 0
						bitEndInclusive = fieldSizeInBits-1	# inclusive
						bitsLeft = containerSizeInBits - fieldSizeInBits
					elif fieldSizeInBits > 0:
						bitStart = bitEndInclusive + 1
						bitEndInclusive = bitStart + fieldSizeInBits-1	# inclusive
						bitsLeft = bitsLeft - fieldSizeInBits
					elif fieldSizeInBits == 0:
						bitsLeft = 0
					else:
						errorMessage ="ERROR: Should never been here during bitfield population"
						errorRoutine(errorMessage)
						return False
		
				if bitsLeft <0:
					errorMessage ="ERROR: bitsLeft (%d) for component # N=%d should never be less than 0"%(bitsLeft,N)
					errorRoutine(errorMessage)
					return False
			
				structMemberIsBitfield[N].append([bitStart,bitEndInclusive])
				structMemberIsBitfield[N].append(containerNumber)
			N += 1		

		# It should print something like [True, basetype, bitfieldwidth,[bitFieldSequenceStartComponent#,bitFieldSequenceEndComponent#],
		#								  [largestContainerDatatype, largestContainerSizeInBytes], [bitStart,bitEndInclusive], containerNumber]
		#   {
		#	 False,
		#	 False,
		#	 [True, int  , 3,[2,2],[int,4],[ 0, 2],0],
		#	 False,
		#	 [True, int  ,10,[4,5],[int,4],[ 0, 9],0],
		#	 [True, short, 5,[4,5],[int,4],[10,14],0],
		#	 False
		#	]
		PRINT ("\n"*3,"After updating the actual bitfield packing details, structMemberIsBitfield =")
		PRINT ("==="*50)
		for item in structMemberIsBitfield:
			PRINT (item)
		PRINT ("==="*50)
		PRINT("\n"*3)

		# Recall that a single structure can have MANY bitfield sequences, and each sequence can potentially require multiple containers
		totalNumContainersForStruct = 0
		N = 0
		while (N<len(structMemberIsBitfield)):
			if structMemberIsBitfield[N] != False: 	# Don't use True, we have a list there instead
				if N == structMemberIsBitfield[N][3][1]:	# Last item in the sequence, which is the fourth item in structMemberIsBitfield
					numContainersRequired = structMemberIsBitfield[N][6] + 1
					currentBitFieldSequence = structMemberIsBitfield[N][3]	# The current bitfield sequence starts from this struct component # and ends at this struct component #
					for t in range (currentBitFieldSequence[0],currentBitFieldSequence[1]+1):
						containerNumber = structMemberIsBitfield[t][-1]
						del structMemberIsBitfield[t][-1]
						structMemberIsBitfield[t].append([containerNumber,numContainersRequired])
					totalNumContainersForStruct += numContainersRequired
			N += 1

		# It should print something like [True, basetype, bitfieldwidth,[bitFieldSequenceStartComponent#,bitFieldSequenceEndComponent#],
		#								  [largestContainerDatatype, largestContainerSizeInBytes], [bitStart,bitEndInclusive], [containerNumber,numContainersRequired]]
		#   {
		#	 False,
		#	 False,
		#	 [True, int  , 3,[2,2],[int,4],[ 0, 2],[0,1]],
		#	 False,
		#	 [True, int  ,10,[4,5],[int,4],[ 0, 9],[0,1]],
		#	 [True, short, 5,[4,5],[int,4],[10,14],[0,1]],
		#	 False
		#	]
		PRINT ("\n"*3,"After updating the [container index, total number of containers] details at the end, structMemberIsBitfield =")
		PRINT ("==="*50)
		for item in structMemberIsBitfield:
			PRINT (item)
		PRINT ("==="*50)
		PRINT("\n"*3)
		
		# Create a dictionary with all these information and later add it to the struct component list member

		N = 0
		while (N<len(structMemberIsBitfield)):
			if structMemberIsBitfield[N] != False: 	# Don't use True, we have a list there instead
				bitFieldInfo = {}
				bitFieldInfo["structComponentIndex"] = N
				bitFieldInfo["structComponentIndexCurrentBitFieldSequenceStart"] = structMemberIsBitfield[N][3][0]
				bitFieldInfo["structComponentIndexCurrentBitFieldSequenceEndInclusive"] = structMemberIsBitfield[N][3][1]
				bitFieldInfo["currentBitFieldSequenceContainerDatatype"] = structMemberIsBitfield[N][4][0]
				bitFieldInfo["currentBitFieldSequenceContainerSizeInBytes"] = structMemberIsBitfield[N][4][1]
				bitFieldInfo["currentBitFieldSequenceContainerIndex"] = structMemberIsBitfield[N][6][0]
				bitFieldInfo["currentBitFieldSequenceTotalNumberOfContainersReqd"] = structMemberIsBitfield[N][6][1]
				bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"] = structMemberIsBitfield[N][5][0]
				bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"] = structMemberIsBitfield[N][5][1]

				structuresAndUnionsDictionary[structName]["components"][N][4]["bitFieldInfo"] = bitFieldInfo
			N += 1
			
		PRINT ("Updated the structuresAndUnionsDictionary[",structName,"][\"components\"] with the following bitfield information:")
		PRINT ("The display has this format:")
		PRINT ("component list member Index, [ isBitField, baseType, bitFieldWidth, [current bitField sequence component list member Index start, end (inclusive)],", 
				"[for current bitfield sequence container type, container size in bytes], [within current container bit index start, end (inclusive)],",
				"[current container index, total number of containers needed for current bit sequence]]")
		N = 0
		while (N<len(structuresAndUnionsDictionary[structName]["components"])):
			structMemberDescription = structuresAndUnionsDictionary[structName]["components"][N][4]
			if structMemberDescription["isBitField"] == False:
				PRINT(N,"False")
			else:
				if "bitFieldInfo" not in getDictKeyList(structMemberDescription):
					errorMessage = "ERROR in coding: \"bitFieldInfo\" not in structMemberDescription.keys() for structName "+structName
					errorRoutine(errorMessage)
					return False
				bitFieldInfo = structuresAndUnionsDictionary[structName]["components"][N][4]["bitFieldInfo"]
#				PRINT (N, bitFieldInfo)
				listToPrint = []
				listToPrint.extend([structMemberDescription["isBitField"],structMemberDescription["baseType"],structMemberDescription["bitFieldWidth"]])
				listToPrint.append([bitFieldInfo["structComponentIndexCurrentBitFieldSequenceStart"],bitFieldInfo["structComponentIndexCurrentBitFieldSequenceEndInclusive"]])
				listToPrint.append( [bitFieldInfo["currentBitFieldSequenceContainerDatatype"], bitFieldInfo["currentBitFieldSequenceContainerSizeInBytes"] ])
				listToPrint.append([bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"],bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"]])
				listToPrint.append([bitFieldInfo["currentBitFieldSequenceContainerIndex"],bitFieldInfo["currentBitFieldSequenceTotalNumberOfContainersReqd"]])
				PRINT(N,listToPrint)
				if listToPrint != structMemberIsBitfield[N]:
					PRINT("listToPrint =",listToPrint)
					PRINT("structMemberIsBitfield[",N,"] = ",structMemberIsBitfield[N])
					errorMessage = "ERROR in coding: listToPrint != structMemberIsBitfield["+STR(N)+"] for structName "+structName
					errorRoutine(errorMessage)
					return False
				
			N += 1
		PRINT("\n"*3)
		PRINT ("==="*50)
		PRINT("\n"*3)
		
		#####################################
		#  Iterate over all struct members  #
		#####################################


		# We define these two variables outside the while loop (for every component member) so that they are within scope for every member
		leadingPadSizeBytes = 0	
		trailingPadSizeBytes = 0
		trailingPadSizeBits = 0
		
		largestMemberLevelAlignment = 1	# The minimum possible alignment. it will get adjusted to the biggest member alignment, unless packed.
			
		# TO-DO: What if the struct has only one component variable? In that case, would the len() return 1, or the number of tokens in the list representing the only component?
		structComponentList = structuresAndUnionsDictionary[structName]["components"]
		N = 0
		# Beware of one thing: if the structure contains N members, out of which B number of members are bitfields, it will not iterate N times - it will iterate N-B+1 times.
		# Basically, when you reach a bitfield, it will process ALL the bitfield components one after another without coming back here.
		# Hence the structuresAndUnionsDictionary[structName]["components"][N][4]["offsetWithinStruct"] needs to be manually updated for bitfield members.
		while (N<len(structuresAndUnionsDictionary[structName]["components"])):
			# First, update within the actual struct dictionary what would be the offsets of that struct component
			if structuresAndUnionsDictionary[structName]["type"]=="union":
				structuresAndUnionsDictionary[structName]["components"][N][4]["offsetWithinStruct"] = 0
			elif structuresAndUnionsDictionary[structName]["type"]=="struct":
				if N == 0:	# The first member of a struct should always have the offset of 0
					structuresAndUnionsDictionary[structName]["components"][N][4]["offsetWithinStruct"] = 0
				else:
					structuresAndUnionsDictionary[structName]["components"][N][4]["offsetWithinStruct"] = structSizeBytes	#Only the first member in a bitfield sequence is getting updated
				pass	# We will update this later with padding. Padding does not apply to unions since in a union, all members start at offset 0
			else:
				PRINT ("Coding ERROR in parseStructure() - Neiher struct nor union!!!!")
				sys.exit()
				
			structMember = structComponentList[N]
			PRINT ("Adding size from structMember =",structMember )
			structMemberName 				= structMember[0]
			structMemberSizeBytes 			= structMember[1]
			structMemberDescription 		= structMember[4]
			if structMemberDescription["isArray"]:
				structMemberNameDatatype 		= structMemberDescription["datatype"]
				structMemberNameDatatypeSize 	= getDatatypeSize(structMemberNameDatatype)
			elif structMemberDescription["isBitField"]:
				bitFieldInfo = structMemberDescription["bitFieldInfo"]
				if N != bitFieldInfo["structComponentIndexCurrentBitFieldSequenceStart"]:
					errorMessage = "ERROR: We should only visit the first member in any bitfield sequence as the cumulative size requirement info is available from there itself"
					errorRoutine(errorMessage)
					return False
				else:
					# These are the "aggregate" variable that remain constant for a bitfield sequence. Like from which component the bitfield sequence starts/ends,
					# how many total containers are required etc.
					structComponentIndexCurrentBitFieldSequenceEndInclusive = bitFieldInfo["structComponentIndexCurrentBitFieldSequenceEndInclusive"]
					currentBitFieldSequenceTotalNumberOfContainersReqd = bitFieldInfo["currentBitFieldSequenceTotalNumberOfContainersReqd"]
					currentBitFieldSequenceContainerSizeInBytes = bitFieldInfo["currentBitFieldSequenceContainerSizeInBytes"]
					structMemberNameDatatypeSize 	= currentBitFieldSequenceTotalNumberOfContainersReqd * currentBitFieldSequenceContainerSizeInBytes
					
					# Update the ["offsetWithinStruct"] for all the subsequent members in the bitfield sequence (recall that the first one is alredy updated)
					# Observe that currentBitFieldSequenceContainerIndex is not an aggregate variable, so it must be updated individually for each component
					for bitFieldSequenceIndex in range(N+1, structComponentIndexCurrentBitFieldSequenceEndInclusive+1):
						if structuresAndUnionsDictionary[structName]["components"][bitFieldSequenceIndex][0] == dummyZeroWidthBitfieldNamePrefix:
							pass
						else:
#							PRINT(structuresAndUnionsDictionary[structName]["components"][bitFieldSequenceIndex][4])
							currentBitFieldSequenceContainerIndex = structuresAndUnionsDictionary[structName]["components"][bitFieldSequenceIndex][4]["bitFieldInfo"]["currentBitFieldSequenceContainerIndex"]
							bitFieldOffsetWithinStruct = structSizeBytes + currentBitFieldSequenceContainerSizeInBytes * currentBitFieldSequenceContainerIndex
							structuresAndUnionsDictionary[structName]["components"][bitFieldSequenceIndex][4]["offsetWithinStruct"] = bitFieldOffsetWithinStruct
				# For bitfield, we are NOT going to iterate over each member in a bitfield sequence - we are just going to plug the value for the whole sequence
				structMemberSizeBytes = bitFieldInfo["currentBitFieldSequenceContainerSizeInBytes"] * bitFieldInfo["currentBitFieldSequenceTotalNumberOfContainersReqd"]
			else:
				structMemberNameDatatypeSize 	= structMemberSizeBytes

			PRINT("\nNow going to calculate the amount of compiler padding. Current structSizeBytes =",structSizeBytes)
			PRINT("For structMemberName =",structMemberName,"structMemberNameDatatypeSize = ",structMemberNameDatatypeSize, "structMemberSizeBytes =", structMemberSizeBytes)

			
			
			# Sanity check
			if structMemberSizeBytes != structuresAndUnionsDictionary[structName]["components"][N][1]:
				PRINT("For structMemberName =",structMemberName,"structMemberNameDatatypeSize = ",structMemberNameDatatypeSize, "structMemberSizeBytes =", structMemberSizeBytes," does not match structuresAndUnionsDictionary[structName][\"components\"][",N,"][1] =", structuresAndUnionsDictionary[structName]["components"][N][1],"isArray =",structuresAndUnionsDictionary[structName]["components"][N][4]["isArray"])
				PRINT("Unless isArray == True above, this is a problem")

	
			
			#########################################################################################################
			# Alignment and Size calculation - Exactly from where it will start to occupy (causes leading padding)
			#########################################################################################################
			
			# 1. First, get the member's datatype's size - that is its natural alignment. For array variables, take the base datatype, not the total size of the array.
			#    For member variables that are struct, take the overall struct's alignment.
			# 2. If there is a member-level or struct-level __attribute__((packed)) statement, it tells that the compiler should start packing the member from the 
			#    first available empty space. You cannot specify a byte-boundary - it's assumed to be 1. So, __attribute__((packed)) overrides natural alignment.
			# 3. __attribute__((aligned(m)))__ overrides __attribute__((packed)) - no matter if the packed is at the struct-level at the member-level.
			#    Once again, recall that the packed doesn't come with a number.
			# 4. #pragma packed(n), when smaller, overrides __attribute__((aligned(m))). It only reduces, but never increases the aligned. So, if n > m, it is ignored.
			
			# If the member item is a struct itself, get its alignment. Recall that unless packed, a structure's alignment is its largest sized member vairable's alignment.
			
			datatype = structuresAndUnionsDictionary[structName]["components"][N][4]["datatype"]
			memberAlignment = 1	# Default value
			sanityCheckCount = 0
			
			# 1. get the "natural" alignment
			while (True):
				sanityCheckCount += 1
				if sanityCheckCount > 100:
					errorMessage = "ERROR in parseStructure() - endlessly looping trying to find the alignment for this member"
					errorRoutine(errorMessage)
					return False
					
				if datatype.startswith("unsigned"):
					datatype = datatype[len("unsigned")+1:]
				elif datatype.startswith("function"): # A function pointer has a size. A function does not need any storage. Pure C does not allow structs to have functions in them.
					memberAlignment = 1		# Possible bug?
					break
				elif datatype in getDictKeyList(primitiveDatatypeLength):
					memberAlignment = primitiveDatatypeLength[datatype]
					break
				elif datatype in getDictKeyList(typedefs):
					# It typedefs into a structure/union
					if isinstance(typedefs[datatype],list) and len(typedefs[datatype])==2 and (typedefs[datatype][0] == "enum" or typedefs[datatype][0] == "struct" or typedefs[datatype][0] == "union"):
						datatype = typedefs[datatype][1]
					# It typedefs into some other regular variable declaration
					else: 
						item = typedefs[datatype]
						PRINT ("The typedef", datatype,"resolves into",item )
						if len(item) != 5:
							errorMessage = "ERROR in parseStructure() - unknown tuple - exiting"
							errorRoutine(errorMessage)
							return False
						else:
							memberAlignment = typedefs[datatype][1]
							break
				elif datatype in getDictKeyList(enums):
					if "attributes" in getDictKeyList(enums[datatype]) and ALIGNED_STRING in getDictKeyList(enums[datatype]["attributes"]):
						memberAlignment = enums[datatype]["attributes"][ALIGNED_STRING]
						break
					else:
						# In C, enum sizes are not specified of at least an INT
						memberAlignment = primitiveDatatypeLength["int"]
						PRINT ("The size of Enum <",datatype,"> is assumed to be same as an Integer,",size )
						break
				elif datatype in getDictKeyList(structuresAndUnionsDictionary):
					structOrUnionName = datatype
					if "attributes" not in getDictKeyList(structuresAndUnionsDictionary[structOrUnionName]):
						errorMessage = "ERROR in parseStructure() - struc/union datatype <" + structOrUnionName + "> does not have attributes - exiting"
						errorRoutine(errorMessage)
						return False
					elif ALIGNED_STRING not in getDictKeyList(structuresAndUnionsDictionary[structOrUnionName]["attributes"]):
						errorMessage = "ERROR in parseStructure() - struc/union datatype <" + structOrUnionName + "> attributes does not have ALIGNED_STRING - exiting"
						errorRoutine(errorMessage)
						return False
					else:
						memberAlignment = int(structuresAndUnionsDictionary[structOrUnionName]["attributes"][ALIGNED_STRING])
						break

			# 2. If there is a struct-level or member-level packed statement, that overrides this natural alignment to 1
			if "attributes" in getDictKeyList(structuresAndUnionsDictionary[structName]) and PACKED_STRING in getDictKeyList(structuresAndUnionsDictionary[structName]["attributes"]):
				memberAlignment = 1
			if "attributes" in getDictKeyList(structuresAndUnionsDictionary[structName]["components"][N][4]) and PACKED_STRING in getDictKeyList(structuresAndUnionsDictionary[structName]["components"][N][4]["attributes"]):
				memberAlignment = 1

			# 3. However, if there is any member-level aligned statement, that overrides this (it cannot decrease, only increase)
			if "attributes" in getDictKeyList(structuresAndUnionsDictionary[structName]["components"][N][4]) and ALIGNED_STRING in getDictKeyList(structuresAndUnionsDictionary[structName]["components"][N][4]["attributes"]):
				memberAlignment = max(memberAlignment,structuresAndUnionsDictionary[structName]["components"][N][4]["attributes"][ALIGNED_STRING])

			
			# 4. #pragma packed(n) overrides the maximum alignment. It only reduces, but never increases the aligned. So, if n > m, it is ignored.
			if pragmaPackCurrentValue != None:
				memberAlignment = min(pragmaPackCurrentValue, memberAlignment)

			# Update the overall struct-level alignment
			largestMemberLevelAlignment = max(memberAlignment, largestMemberLevelAlignment)

			# Once we know the alignment, calculate its effective size. It must be at least as big as the natural size, otherwise we will lose data
			effectiveSize = max(structMemberSizeBytes, memberAlignment)

			PRINT("After processing struct member",structMemberName,"of original structMemberSizeBytes =",structMemberSizeBytes,"and effectiveSize =",effectiveSize,"and member-level alignment =",memberAlignment,"set largestMemberLevelAlignment = ",largestMemberLevelAlignment) 


			# Every struct member may have some leading padding and some trailing padding. The trailing padding may be re-used by the next struct item,
			# if it does not violate the alignment rules for the next struct item. However, irrespective of if any part of the the trailing pads for a struct member 
			# is used by the next member or not, the trailing parts are to be counted in the overall struct length.
			# Suppose the current structSizeBytes = 10, current trailingPadSizeBytes = 3 and the next item C is a char. The whole of the next item C will fit in this traling pad,
			# so after consuming this C the structSizeBytes = 10 (no change), but trailingPadSizeBytes = 2 (changed).
			# Remember, the structSizeBytes is already inclusive of the trailing paddings for the previous member.
			# So we first find out where did the REAL data (from the previous member ended)
			
			if structuresAndUnionsDictionary[structName]["type"]=="struct":


				if structMemberDescription["isBitField"] == True:
				
					bitFieldWidth = structComponentList[N][4]["bitFieldWidth"]
					
					previousMemberEndedAtSizeBits = structSizeBytes * BITS_IN_BYTE - trailingPadSizeBits
					PRINT ("The previous struct member ended at struct size = ", previousMemberEndedAtSizeBits,"bits")
					if previousMemberEndedAtSizeBits > 0:
						previousMemberEndedAtSizeBytes = integerDivision(previousMemberEndedAtSizeBits,BITS_IN_BYTE)
						PRINT ("Which means the last populated data is at Byte #",previousMemberEndedAtSizeBytes,", bit #", previousMemberEndedAtSizeBits - previousMemberEndedAtSizeBytes*BITS_IN_BYTE - 1)
#					PRINT ("Currently handling struct member #",N,"(",structMemberName,") of structMemberSizeBytes =",structMemberSizeBytes,"and memberAlignment =",memberAlignment,"offsetWithinStruct=",offsetWithinStruct,"leadingPadSizeBytes =",leadingPadSizeBytes,"trailingPadSizeBytes =",trailingPadSizeBytes,"structSizeBytes =",structSizeBytes)
					PRINT ("Currently handling struct member #",N,"(",structMemberName,") of structMemberSizeBytes =",structMemberSizeBytes,"and memberAlignment =",memberAlignment,"leadingPadSizeBytes =",leadingPadSizeBytes,"trailingPadSizeBytes =",trailingPadSizeBytes,"structSizeBytes =",structSizeBytes)
					if structMemberDescription["baseType"] not in ("char","short","int","long","long long"):
						errorMessage = "ERROR: struct " + structName + " has a bitfield member " + structMemberName + " with unsupported baseType = " + structMemberDescription["baseType"]
						errorRoutine(errorMessage)
						return False
					else:
						PRINT("For struct", structName, "member", structMemberName, "with baseType", structMemberDescription["baseType"],"(width ",primitiveDatatypeLength[structMemberDescription["baseType"]],"), Current memberAlignment =",memberAlignment)
						
					# If there is any __attribute__((aligned(m))) for this bitfield member (where the alignment value m might be reduced by a #pragma pack(n) statement),
					# Then we absolutely need to adhere to the alignment width. Otherwise, use the regular packing.
					if "attributes" in getDictKeyList(structuresAndUnionsDictionary[structName]["components"][N][4]) and ALIGNED_STRING in getDictKeyList(structuresAndUnionsDictionary[structName]["components"][N][4]["attributes"]):
						memberAlignmentBits = memberAlignment * BITS_IN_BYTE
						
						# If the bitfield width is bigger than the memberAlignmentBits, then we need to up it to the level.
						# For example, we cannot ask a short s:9 to be aligned to 8 bits - it must be upped to 16 bits.
						while True:
							if bitFieldWidth > memberAlignmentBits:
								memberAlignmentBits *= 2
							else:
								break
						PRINT("For struct", structName, "member", structMemberName, "with baseType", structMemberDescription["baseType"],"and bitFieldWidth =",bitFieldWidth,", Current memberAlignmentBits =",memberAlignmentBits)
						
						# Not sure what I was trying to do here
						'''
						# Find which bit we should start packing this bitfield from
						if previousMemberEndedAtSizeBits == 0:
							startPackingFromBit = 0
						else:
							count = -1
							while (True):
								count += 1
								if memberAlignmentBits * count - 1 > previousMemberEndedAtSizeBits:
									startPackingFromBit = memberAlignmentBits * count - 1
									break
						'''
						
					structSizeBytes += structMemberSizeBytes
					
				elif structMemberDescription["isBitField"] == False:
					# You have to be careful while utilizing the potential possible padding. Recall that a member may use the previous traling padding.
					# And, if the previous padding padding is enough for accommodating the current struct member, the overall length of the struct may not increase at all.
					# Heck, it is even possible that after packing the current item, there will be still some trailing padding left.
					# For example, look here below. Here, just after processing c1 the overall struct length is 4, with 3 traling padding. 
					# Then after c2 is processed, the overall struct length is still 4, with 2 traling padding.
					# 
					#   struct A { 
					#  				char c1 __attribute__((aligned(4)));
					#  				char c2 ;
					#			};

					previousMemberEndedAtSizeBytes = structSizeBytes - trailingPadSizeBytes 	# This trailingPadSizeBytes was calculated by the previous struct member in previous iteration
					
					PRINT ("Although currently structSizeBytes =",structSizeBytes,"trailingPadSizeBytes =",trailingPadSizeBytes,"which means previousMemberEndedAtSizeBytes =",previousMemberEndedAtSizeBytes)
					
					# First find out exactly where the current member data starts
					leadingPadSizeBytes = 0 if previousMemberEndedAtSizeBytes % memberAlignment == 0 else memberAlignment - (previousMemberEndedAtSizeBytes % memberAlignment)
					offsetWithinStruct = previousMemberEndedAtSizeBytes + leadingPadSizeBytes
					PRINT ("For previousMemberEndedAtSizeBytes =",previousMemberEndedAtSizeBytes,"memberAlignment =",memberAlignment,"leadingPadSizeBytes =",leadingPadSizeBytes,", resulting in offsetWithinStruct =",offsetWithinStruct)
					
					currentMemberRealDataEndByte  = offsetWithinStruct + structMemberSizeBytes	# thanks to an aligned(m), a member's size may artifically increase. This is where real data ends
					currentMemberAlignmentEndByte = offsetWithinStruct + effectiveSize
					structSizeBytes = max(structSizeBytes, currentMemberAlignmentEndByte)
					
					# MUST NOT define trailingPadSizeBytes before this since it will be used by the next struct member in next iteration
					# Right in this statement below, we are OVERWRITING the trailingPadSizeBytes
					trailingPadSizeBytes = structSizeBytes - currentMemberRealDataEndByte
					trailingPadSizeBits = trailingPadSizeBytes * BITS_IN_BYTE

					structuresAndUnionsDictionary[structName]["components"][N][4]["offsetWithinStruct"] = offsetWithinStruct	#Only the first member in a bitfield sequence is getting updated
					
					PRINT ("After processing struct member #",N,"(",structMemberName,") of structMemberSizeBytes =",structMemberSizeBytes,"and memberAlignment =",memberAlignment,"offsetWithinStruct=",offsetWithinStruct,"leadingPadSizeBytes =",leadingPadSizeBytes,"currentMemberRealDataEndByte (",currentMemberRealDataEndByte, ") + trailingPadSizeBytes (",trailingPadSizeBytes,") = structSizeBytes =",structSizeBytes)
				else:
					errorMessage = "ERROR: For structuresAndUnionsDictionary[\"%s\"], structMemberDescription[\"isBitField\"] = %s, not either True or False"%(structName,structMemberDescription["isBitField"])
					errorRoutine(errorMessage)
					return False
					
				
			elif structuresAndUnionsDictionary[structName]["type"]=="union":
				structSizeBytes = structMemberSizeBytes if structMemberSizeBytes >  structSizeBytes else structSizeBytes
			else:
				errorMessage = "ERROR: structuresAndUnionsDictionary[\"%s\"][\"type\"] = %s, not either \"struct\" or \"union\""%(structName,structuresAndUnionsDictionary[structName]["structOrUnion"])
				errorRoutine(errorMessage)
				return False

				
			# If it is bitfield, we have already gotten the summary data for the current bitfield sequence, hence just go to the item after that
			if structMemberDescription["isBitField"]:
				N = structComponentIndexCurrentBitFieldSequenceEndInclusive + 1
			else:
				N = N + 1
				
#			PRINT("Manna After calculating the amount of compiler padding for structMemberName =",structMemberName,", bytesToPad =",bytesToPad,", Current structSizeBytes =",structSizeBytes)
			PRINT("After calculating the amount of compiler padding for structMemberName =",structMemberName,", trailingPadSizeBytes =",trailingPadSizeBytes,", Current structSizeBytes =",structSizeBytes)

		# Now add the struct-level traling bytes, if required

		# 1. First we set the struct-level alignment as the largest member-level alignment
		# 2. Next, if there is any struct-level alignment statement, that overrides it
		
		PRINT("\n\n","==="*50,"End-Of-Struct processing","==="*50,"\n\n")
		PRINT("largestMemberLevelAlignment =",largestMemberLevelAlignment)
		if "attributes" in getDictKeyList(structuresAndUnionsDictionary[structName]) and PACKED_STRING in getDictKeyList(structuresAndUnionsDictionary[structName]["attributes"]):
			PRINT("There is a struct-level __attribute__((packed)), but we do nothing with it since its effect has been transmitted to each struct member")
		structLevelAlignment = largestMemberLevelAlignment
		PRINT("structLevelAlignment is set to the largestMemberLevelAlignment =", structLevelAlignment)

		if "attributes" in getDictKeyList(structuresAndUnionsDictionary[structName]) and ALIGNED_STRING in getDictKeyList(structuresAndUnionsDictionary[structName]["attributes"]):
			structLevelAlignedValue = structuresAndUnionsDictionary[structName]["attributes"][ALIGNED_STRING]
			structLevelAlignment = max(structLevelAlignment, structLevelAlignedValue)	# Aligned() can only increase an alignment
			PRINT("There is a struct-level __attribute__((aligned(",structLevelAlignedValue,"))), hence now structLevelAlignment =",structLevelAlignment)

		if pragmaPackCurrentValue != None:
			structLevelAlignment = min(pragmaPackCurrentValue, structLevelAlignment)
			PRINT("There is a #pragma pack(",pragmaPackCurrentValue,") statement, hence now structLevelAlignment =",structLevelAlignment)
			
		PRINT("Final value of structLevelAlignment =",structLevelAlignment)

		if structSizeBytes % structLevelAlignment != 0:
			structLevelTrailingPads = structLevelAlignment - (structSizeBytes % structLevelAlignment)
			PRINT ("Adding structLevelTrailingPads =",structLevelTrailingPads,"to the current structSizeBytes=",structSizeBytes)
			structSizeBytes += structLevelTrailingPads
			PRINT("Final structSizeBytes =",structSizeBytes)

		# After processing ALL the members for a struct
		
		if "attributes" in getDictKeyList(structuresAndUnionsDictionary[structName]):
			if ALIGNED_STRING in getDictKeyList(structuresAndUnionsDictionary[structName]["attributes"]):
				PRINT("structuresAndUnionsDictionary[structName][\"attributes\"][ALIGNED_STRING] already exists",structuresAndUnionsDictionary[structName]["attributes"])
				PRINT("Overwriting its current value (",structuresAndUnionsDictionary[structName]["attributes"][ALIGNED_STRING],") with new structLevelAlignment value = ",structLevelAlignment)
				structuresAndUnionsDictionary[structName]["attributes"][ALIGNED_STRING] = structLevelAlignment
			else:
				PRINT("structuresAndUnionsDictionary[structName][\"attributes\"][ALIGNED_STRING] did not exist in",structuresAndUnionsDictionary[structName]["attributes"])
				PRINT("Setting it to structLevelAlignment value = ",structLevelAlignment)
				structuresAndUnionsDictionary[structName]["attributes"][ALIGNED_STRING] = structLevelAlignment
		else:
			PRINT("structuresAndUnionsDictionary[structName][\"attributes\"] did not exist")
			PRINT("Setting it to {ALIGNED_STRING: structLevelAlignment value (",structLevelAlignment,") }")
			attributes = {ALIGNED_STRING:structLevelAlignment}
			structuresAndUnionsDictionary[structName]["attributes"] = attributes
			
		PRINT ("After completing processing, struct-level attribute =", structuresAndUnionsDictionary[structName]["attributes"])
		
		'''
		if STRUCT_END_PADDING_ON == True and structSizeBytes >= 3 and structSizeBytes%4 > 0:
			structSizeBytes += (4 - (structSizeBytes%4))
		'''
		
		structuresAndUnionsDictionary[structName]["size"] = structSizeBytes
		
		PRINT ("structuresAndUnionsDictionary[",structName,"][\"size\"]=", structuresAndUnionsDictionary[structName]["size"] )
		
		
		
		return structName

# Custom print function for the unraveled list since we do not want to print the whole of variableDescription dictionary, which is the third item in each row
def printUnraveled():
	PRINT ("\n\n","=="*100,"\nunraveled (level, variable, datatype, starting offset (inclusive), ending offset+1 (exclusive) \n","=="*100,"\n", )
	for row in unraveled:
		rowText = "["+STR(row[0])
		for N in range(1,len(row)):
			item = row[N]
			if N == 2 and isinstance(row[N],dict):
				try:
					rowText += ", "+item["datatype"]
				except KeyError:
					OUTPUT ("KeyError in printUnraveled() for N=",N," row[N] =",item)
			else:
				rowText += ", "+STR(item)
		rowText += "]"
		PRINT (rowText)
	PRINT ("\n\n","=="*100 )

#######################################################################################################
# unravelNestedStruct(structName, prefix)
########################################################################################################
def unravelNestedStruct(level, structName, prefix, offset):
	global unraveled
	PRINT ("\n\nInside unravelNestedStruct(",structName,",",prefix,",",STR(offset),"), unraveled = ")
	printUnraveled()
	
	if structName not in getDictKeyList(structuresAndUnionsDictionary):
		errorMessage = "supplied struct/union name "+structName+" does not exist - exiting!"
		errorRoutine(errorMessage)
		return False

	structOrUnion = structuresAndUnionsDictionary[structName]["type"]
	structSizeBytes = structuresAndUnionsDictionary[structName]["size"]
	unraveled.append([level,prefix+" is of type "+structOrUnion,structName, offset, offset+structSizeBytes])

	PRINT("Going to iterate over",len(structuresAndUnionsDictionary[structName]["components"]),"components of",structName)
	N = 0
	while N < len(structuresAndUnionsDictionary[structName]["components"]):
		PRINT("Component #",N)
		structMember = structuresAndUnionsDictionary[structName]["components"][N]
		PRINT ("\nInside unravelNestedStruct(), Processing from structMember =",structMember )
		variableName 					= structMember[0]
		structMemberSizeBytes 			= structMember[1]
		structMemberDescription 		= structMember[4]
		baseType						= structMemberDescription["baseType"]
		datatype						= structMemberDescription["datatype"]
		if structMember[0]!=dummyZeroWidthBitfieldNamePrefix:
			offsetWithinStruct 			= structMemberDescription["offsetWithinStruct"]
		PRINT ("\nfor N =",N,"variableName =",variableName,"datatype =",datatype,"structMemberDescription =",structMemberDescription)
#		PRINT ("passed KeyError")
		
		if variableName == dummyZeroWidthBitfieldNamePrefix:
			PRINT("Not adding the dummy variable for resetting the bitfield boundary")
		elif structMemberDescription["isArray"]:
			arrayElementSize = structMemberDescription["arrayElementSize"]
			arrayDimensions = structMemberDescription["arrayDimensions"]
			totalNumberOfArrayElements = listItemsProduct(arrayDimensions)
			dimensionsText = str(arrayDimensions[0])
			for d in range(1,len(arrayDimensions)):
				dimensionsText += " X "+ str(arrayDimensions[d])
			
			dataTypeText = "unsigned" + " " + datatype if datatype != "pointer" and structMemberDescription["signedOrUnsigned"] == "unsigned" else datatype
			arrayDescriptionText = prefix + "." + variableName + " - Array of "+ dimensionsText + " " + dataTypeText + "s"
			unraveled.append([level+1,arrayDescriptionText,structMemberDescription, offset+offsetWithinStruct, offset+offsetWithinStruct+arrayElementSize*totalNumberOfArrayElements])
			for position in range(totalNumberOfArrayElements):
				arrayIndices = calculateArrayIndicesFromPosition(arrayDimensions, position)
				arrayIndicesCStyle = ""	# We convert the [i,j,k] to C-style [i][j][k]
				for item in arrayIndices:
					arrayIndicesCStyle += "["+STR(item)+"]"
				arrayElementIndexDescription = STR(variableName) + arrayIndicesCStyle
				elementOffset = offset + offsetWithinStruct + position * arrayElementSize
				if datatype in getDictKeyList(structuresAndUnionsDictionary):
					unravelNestedStruct(level+2, datatype, prefix+"."+arrayElementIndexDescription, elementOffset)
				else:
					unraveled.append([level+2,prefix + "." + arrayElementIndexDescription,structMemberDescription, elementOffset, elementOffset+arrayElementSize])
		elif datatype in getDictKeyList(structuresAndUnionsDictionary):
			PRINT("\ndatatype is struct/union - calling unravelNestedStruct() recursively.")
			unravelNestedStruct(level+1, datatype, prefix+"."+variableName, offset + offsetWithinStruct)
		else:
			PRINT("\ndatatype is",datatype," Adding to unraveled.")
			unraveled.append([level+1, prefix+"."+variableName,structMemberDescription, offset+offsetWithinStruct, offset+offsetWithinStruct+structMemberSizeBytes ])
		N += 1
	PRINT ("\n\nJust before returning from unravelNestedStruct(",structName,",",prefix,",",STR(offset),"), unraveled = ")
	printUnraveled()
	return True	

########################################################################################################################################################
# The logic behind this is the following. It adds the entry for the variableId to the sizeOffsets list, then if this variable is actually overlapping
# with some other struct, then it adds the struct members too.
############################################################################################################################
def getOffsetsRecursively(variableId, sizeOffsets, beginOffset):
	variableName = variableDeclarations[variableId][0]
	variableSize = variableDeclarations[variableId][1]
	datatype     = variableDeclarations[variableId][4]['datatype']
	
	sizeOffsets.append([variableId,beginOffset,variableSize])
	
	if variableDeclarations[variableId][4]["DataOverlapWithStructMembers"]:
		if datatype not in getDictKeyList(structuresAndUnionsDictionary):
			OUTPUT (variableDeclarations[variableId])
			errorMessage = "Error - for variableId = " + variableId + " the datatype = " + datatype + " is not a struct/union"
			return False
		else:	
			structName = datatype
			for component in structuresAndUnionsDictionary[structName]["components"]:
				if component[0] == dummyZeroWidthBitfieldNamePrefix:
					PRINT("Zero-width bitfield - ignoring!")
					PRINT("Component = ", component)
				elif 'offsetWithinStruct' not in getDictKeyList(component[4]):
					OUTPUT ("For variableName =",variableName,", variableDeclarations[variableId] =",variableDeclarations[variableId],"\n"*3)
					OUTPUT ("structuresAndUnionsDictionary[datatype][\"components\"] =",structuresAndUnionsDictionary[datatype]["components"],"\n"*3)	# datatype is same as structName
					OUTPUT ("component =", component,"\n"*3)
					errorMessage = "Error - for variableId = " + variableId + " the struct/datatype = " + datatype + " does not have 'offsetWithinStruct' in its component"
					return False
				else:
					sizeOffsets = getOffsetsRecursively(component[4]["variableId"], sizeOffsets, beginOffset+component[4]['offsetWithinStruct'])
				
	return sizeOffsets


###############################################################################################################
# This function takes in two things: A token index, and a token information triad (output of tokenizeLines()
###############################################################################################################
def fistAndLastTokenIndicesOnSameLineForTokenNumber(tokenIndex, tokenListInformation):

	PRINT("\nTrying to look for the first and last token indices on the same line as the given token index",tokenIndex)
	
	if isinstance(tokenListInformation,list) and (len(tokenListInformation) != 3):
		errorMessage = "ERROR in fistAndLastTokenIndicesOnSameLineForTokenNumber() - supplied tokenListInformation is not a valid list - hence exiting"
		errorRoutine(errorMessage)
		return False
	elif not checkIfIntegral(tokenIndex):
		errorMessage = "ERROR in fistAndLastTokenIndicesOnSameLineForTokenNumber() - supplied tokenIndex"+STR(tokenIndex)+"is not a valid integer - hence exiting"
		errorRoutine(errorMessage)
		return False
	elif tokenIndex <0 or tokenIndex >= len(tokenListInformation[0]):
		errorMessage = "ERROR in fistAndLastTokenIndicesOnSameLineForTokenNumber() - supplied tokenIndex"+STR(tokenIndex)+"is not a valid index - the valid range is <0,"+STR(len(tokenListInformation[0])-1)+">"
		errorRoutine(errorMessage)
		return False
		
	lineStart = tokenListInformation[1][tokenIndex][2][0][0]
	lineEnd   = tokenListInformation[1][tokenIndex][2][-1][0]
	
	PRINT("\nThe token#",tokenIndex,"(",tokenListInformation[0][tokenIndex],") starts on line #",lineStart,"and ends on line #",lineEnd)
	
	firstTokenIndexOnlineStart = tokenListInformation[2][lineStart][0][1]
	lastTokenIndexOnlineEnd    = tokenListInformation[2][lineEnd][-1][1]

	if not checkIfIntegral(firstTokenIndexOnlineStart) or not checkIfIntegral(lastTokenIndexOnlineEnd):
		errorMessage = "ERROR in fistAndLastTokenIndicesOnSameLineForTokenNumber() - the calculated firstTokenIndexOnlineStart ("+STR(firstTokenIndexOnlineStart)+") or lastTokenIndexOnlineEnd ("+STR(lastTokenIndexOnlineEnd)+") is not integral"
		errorRoutine(errorMessage)
		return False
	elif not ( 0<= firstTokenIndexOnlineStart < len(tokenListInformation[0])) or not ( 0<= lastTokenIndexOnlineEnd < len(tokenListInformation[0])):
		errorMessage = "ERROR in fistAndLastTokenIndicesOnSameLineForTokenNumber() - the calculated firstTokenIndexOnlineStart ("+STR(firstTokenIndexOnlineStart)+") or lastTokenIndexOnlineEnd ("+STR(lastTokenIndexOnlineEnd)+") is not valid"
		errorRoutine(errorMessage)
		return False
	else:	
		PRINT("The first token on line #",lineStart,"has token index of",firstTokenIndexOnlineStart,", and it is <",tokenListInformation[0][firstTokenIndexOnlineStart],">")
		PRINT("The last  token on line #",lineEnd,  "has token index of",lastTokenIndexOnlineEnd,   ", and it is <",tokenListInformation[0][lastTokenIndexOnlineEnd   ],">")
	
	return [firstTokenIndexOnlineStart,lastTokenIndexOnlineEnd]

################################################################################################################
# Non-Declaration code. Returns the [status,token index of where the next "statement" ends (inclusive).]
# The reason we return two things is because 0 is also a valid index, and 0 often equates to False.
################################################################################################################

def parseRegularNonDeclarationCode(tokenList):
	
	i = 0
	##################    WHILE  / FOR LOOP  / SWITCH  #########################
	if tokenList[i] in ("while", "for", "switch"):
		PRINT(tokenList[i],"found")
	
		loopType = tokenList[i]
	
		if i==len(tokenList)-1 or tokenList[i+1] != "(":
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " loop must have a ( to start with"
			errorRoutine(errorMessage)
			return [False, None]
		elif i+1 == len(tokenList)-1 or ")" not in tokenList[i+2:]:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " loop must have a ) to close the condition"
			errorRoutine(errorMessage)
			return [False, None]
		elif matchingBraceDistance(tokenList[i+1:]) < 1:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " loop must have a matching ) to close the condition"
			errorRoutine(errorMessage)
			return [False, None]
		
		conditionEndBraceIndex = i+1 + matchingBraceDistance(tokenList[i+1:])
		PRINT("conditionEndBraceIndex =",conditionEndBraceIndex, "which means the whole expression is", tokenList[i+1:conditionEndBraceIndex+1])
		
		if conditionEndBraceIndex == len(tokenList)-1:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " must have either a semicolon or matching {} after the while(condition)"
			errorRoutine(errorMessage)
			return [False, None]
		elif tokenList[conditionEndBraceIndex+1] == "{":
			if "}" not in tokenList[conditionEndBraceIndex+1:]:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - no matching {} after the" + loopType + "(condition)"
				errorRoutine(errorMessage)
				return [False, None]
			elif matchingBraceDistance(tokenList[conditionEndBraceIndex+1:])<1:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " body must have a matching } to close the body"
				errorRoutine(errorMessage)
				return [False, None]
			else:
				curlyBraceEndIndex = conditionEndBraceIndex+1 + matchingBraceDistance(tokenList[conditionEndBraceIndex+1:])
				PRINT("Returning curlyBraceEndIndex =",curlyBraceEndIndex, "which means the whole expression is", tokenList[i:curlyBraceEndIndex+1])
				return [True, curlyBraceEndIndex]
		elif tokenList[i] == "switch":
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " must have a pair of curly braces to designate the body"
			errorRoutine(errorMessage)
			return [False, None]
		elif ";" not in tokenList[conditionEndBraceIndex+1:]:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " body must have a semicolon to close the body"
			errorRoutine(errorMessage)
			return [False, None]
		else:
			singleStatementEndIndex = conditionEndBraceIndex+1 + tokenList[conditionEndBraceIndex+1:].index(";") 
			return [True,singleStatementEndIndex]
		
		if loopType in ("for","while") and ";" not in tokenList[conditionEndBraceIndex+1:] and ( tokenList[conditionEndBraceIndex+1] != "{" or "}" not in tokenList[conditionEndBraceIndex+1:]):
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " loop body must have either a semicolon or matching {} after the while(condition)"
			errorRoutine(errorMessage)
			return [False, None]
		elif loopType in ("switch") and (tokenList[conditionEndBraceIndex+1] != "{" or "}" not in tokenList[conditionEndBraceIndex+1:]):
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " body must have either a semicolon or matching {} after the while(condition)"
			errorRoutine(errorMessage)
			return [False, None]
		elif tokenList[conditionEndBraceIndex+1] == "{": 
			if matchingBraceDistance(tokenList[conditionEndBraceIndex+1:])<1:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - " + loopType + " body must have a matching } to close the body"
				errorRoutine(errorMessage)
				return [False, None]
			else:
				whileLoopBodyCurlyBraceEndIndex = conditionEndBraceIndex+1 + matchingBraceDistance(tokenList[conditionEndBraceIndex+1:])
				return whileLoopBodyCurlyBraceEndIndex
		result = parseRegularNonDeclarationCode(tokenList[conditionEndBraceIndex+1:])
		if result[0] == False:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - cannot parse the body for the" + loopType 
			errorRoutine(errorMessage)
			return [False, None]
		else:
			singleStatementEndIndex = conditionEndBraceIndex+1 + result[1] 
			return [True,singleStatementEndIndex]
			

	##################    DO- WHILE  LOOP    #########################
	elif tokenList[i] == "do":		

		if i==len(tokenList)-1 or tokenList[i+1] != "(" and ";" not in tokenList[i+1:] :
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - do-while loop must have a { to start with"
			errorRoutine(errorMessage)
			return [False, None]
		elif tokenList[i+1]=="{":
			if i+1 == len(tokenList)-1 or "}" not in tokenList[i+2:]:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - while loop must have a ) to close the condition"
				errorRoutine(errorMessage)
				return [False, None]
			elif matchingBraceDistance(tokenList[i+1:]) < 1:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - while loop must have a matching ) to close the condition"
				errorRoutine(errorMessage)
				return [False, None]
			doLoopBodyEndIndex = i+1+matchingBraceDistance(tokenList[i+1:])
		else:
			result = parseRegularNonDeclarationCode(tokenList[i+1:])
			if result[0] == False:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - do{body}while(condition); loop must have a proper body"
				errorRoutine(errorMessage)
				return [False, None]
			else:
				doLoopBodyEndIndex = i+1 + result[1]
		
		if doLoopBodyEndIndex >= len(tokenList)-1 or tokenList[doLoopBodyEndIndex+1] != "while":
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - do-while loop must have a while"
			errorRoutine(errorMessage)
			return [False, None]
		elif tokenList[doLoopBodyEndIndex+2]!="(" or ")" not in tokenList[doLoopBodyEndIndex+2:]:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - do-while loop must have a condition after the while keyword"
			errorRoutine(errorMessage)
			return [False, None]
		elif matchingBraceDistance(tokenList[doLoopBodyEndIndex+2:])<0:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - the while() condition in the do-while loop does not have a matching )"
			errorRoutine(errorMessage)
			return [False, None]
		
		doWhileLoopWhileConditionBraceEndIndex = doLoopBodyEndIndex+2 + matchingBraceDistance(tokenList[doLoopBodyEndIndex+2:])
		
		if doWhileLoopWhileConditionBraceEndIndex >= len(tokenList)-1 or tokenList[doWhileLoopWhileConditionBraceEndIndex+1] != ";":
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - the while() condition in the do-while loop does not have a semicolon after that"
			errorRoutine(errorMessage)
			return [False, None]
		else:
			return [True, doWhileLoopWhileConditionBraceEndIndex+1]
		
			
	##################    IF / THEN / ELSE    #########################
	elif tokenList[i] == "if":
	
		ifBodyEndIndex = LARGE_NEGATIVE_NUMBER
		
		if i ==len(tokenList)-1 or tokenList[i+1] != "(" or ")" not in tokenList[i+1:]:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - it does not have proper () after if/else keyword"
			errorRoutine(errorMessage)
			return [False, None]
		elif matchingBraceDistance(tokenList[i+1:])<0:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - it does not have proper matching ) after if/elseif ("
			errorRoutine(errorMessage)
			return [False, None]
			
		conditionEndBraceIndex = i+1+matchingBraceDistance(tokenList[i+1:])
		
		if conditionEndBraceIndex == len(tokenList)-1:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() -  must have either a semicolon or matching {} after the if(condition)"
			errorRoutine(errorMessage)
			return [False, None]
		elif tokenList[conditionEndBraceIndex+1]=="{":
			if conditionEndBraceIndex+1 == len(tokenList)-1 or "}" not in tokenList[conditionEndBraceIndex+2:]:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - if must have a ) to close the condition"
				errorRoutine(errorMessage)
				return [False, None]
			elif matchingBraceDistance(tokenList[conditionEndBraceIndex+1:]) < 1:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - if must have a matching ) to close the condition"
				errorRoutine(errorMessage)
				return [False, None]
			ifBodyEndIndex = conditionEndBraceIndex+1 + matchingBraceDistance(tokenList[conditionEndBraceIndex+1:])
		else:
			result = parseRegularNonDeclarationCode(tokenList[conditionEndBraceIndex+1:])
			if result[0] == False:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - if(condition); must have a proper body"
				errorRoutine(errorMessage)
				return [False, None]
			else:
				ifBodyEndIndex = conditionEndBraceIndex+1 + result[1]
		
		if ifBodyEndIndex == LARGE_NEGATIVE_NUMBER:
			OUTPUT("Coding error in parseRegularNonDeclarationCode() for parsing if")
			sys.exit()
			
		if ifBodyEndIndex == len(tokenList)-1 or tokenList[ifBodyEndIndex+1] != "else":
			return [True, ifBodyEndIndex]
		elif ifBodyEndIndex+2 <= len(tokenList)-1 and tokenList[ifBodyEndIndex+2] == '{':
			if '}' not in tokenList[ifBodyEndIndex+3:]:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - if(condition); else lacks the ending }"
				errorRoutine(errorMessage)
				return [False, None]
			result = matchingBraceDistance(tokenList[ifBodyEndIndex+2:])
			if result < 1:
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - if(condition)else must have a matching ) to close the else {"
				errorRoutine(errorMessage)
				return [False, None]
			else:
				elseBodyEndIndex = ifBodyEndIndex+2+result
				return [True, elseBodyEndIndex]
		else:
			PRINT("Calling parseRegularNonDeclarationCode() for",STR(tokenList[ifBodyEndIndex+2:]))
			result = parseRegularNonDeclarationCode(tokenList[ifBodyEndIndex+2:])
			PRINT("Result is",result)
			if result[0] == False:
				PRINT("Result is",result,"!")
				errorMessage = "ERROR in parseRegularNonDeclarationCode() - if(condition) else must have a proper body"
				errorRoutine(errorMessage)
				return [False, None]
			else:
				elseBodyEndIndex = ifBodyEndIndex+2 + result[1]
				return [True, elseBodyEndIndex]
				
	else:
	
		# Check for assignments. Make sure that it is at the "open", i.e. not enclosed by any parentthesis, like func1(int i=0){}, which is NOT an assignment
		if ';' in tokenList[i:] and '=' in tokenList[i:] and tokenList[i:].index("=") < tokenList[i:].index(";"):
			# make a temporary copy of the tokenList upto the semicolon
			list1 = tokenList[i:tokenList[i:].index(";")+1]
			list2 = list1
			numItemsDeleted = 0
			j = 0
			while j<len(list1):
				if list1[j] in ('(','{','['):
					d = matchingBraceDistance(list1[j])
					if d<0:
						errorMessage = "ERROR in parseRegularNonDeclarationCode() - unmatched "+list1[j]+" in assignment"
						errorRoutine(errorMessage)
						return [False, None]
					else:
						del list2[j-numItemsDeleted:j+d+1-numItemsDeleted]
						numItemsDeleted += d+1
						j = j + d
				j += 1
			if '=' in list2:
				PRINT("Found assigment")
				return [True, i + tokenList[i:].index(";")]
				
		# Check for function definitions
		if '(' in tokenList[i:] and ')' in tokenList[i:] and '{' in tokenList[i:] and '}' in tokenList[i:]:
			j = i+tokenList[i:].index("(")
			if j>0 and tokenList[j-1] not in illegalVariableNames and matchingBraceDistance(tokenList[j:]) > 0 and tokenList[j+matchingBraceDistance(tokenList[j:])+1]=='{' and '}' in tokenList[j+matchingBraceDistance(tokenList[j:])+2:]:
			   return [True, j+matchingBraceDistance(tokenList[j:])+1+matchingBraceDistance(tokenList[j+matchingBraceDistance(tokenList[j:])+1:])]
			   
		# Any other statement ending with a semicolon
		if ';' not in tokenList[i:]:
			errorMessage = "ERROR in parseRegularNonDeclarationCode() - unknown tokenstream" + STR(tokenList[i:])
			errorRoutine(errorMessage)
			return [False, None]
		else:
			PRINT("Returning",i+tokenList[i:].index(";"))
			return [True, i+tokenList[i:].index(";")]
		
###########################################################################################################
# This function takes in a tokenList and parses it	
# All #define macro invokations have already been done by preprocess(). So, just ignore any such statement
###########################################################################################################
def parseCodeSnippet(tokenListInformation, rootNode):
	global pragmaPackStack, pragmaPackCurrentValue, typedefs, enums, lines, structuresAndUnionsDictionary, primitiveDatatypeLength, variableDeclarations, dummyVariableCount, totalVariableCount, globalScopes
	# This list contains the different variables that were declared as part of the supplied tokenList
	variableDeclarations = []
	PRINT ("inside parseCodeSnippet" )
	# There could be mixing of #defines and structure/union declarations, and simple variable declaration

	declarationKeywords = ['void','char','short','int','long','long long', 'float','double','signed','unsigned', 'auto','register','static','extern','typedef','const','volatile']
	
	# There are 3 things we get from the input tokenListInformation
	# 1. The simple array of tokens - tokenList
	# 2. Token-wise token information (from which line/char it starts and ends)
	# 3. Line-wise token information (which all tokens are there on that line, and from which line/char each such token starts and ends)
	tokenList = tokenListInformation[0]
	
	# Just to check
	for ti in range(len(tokenList)):
		temp = fistAndLastTokenIndicesOnSameLineForTokenNumber(ti, tokenListInformation)
	
	i = 0;
	while i < len(tokenList):
		PRINT ("Processing tokenList[",i,"] = <%s>"%tokenList[i] )
		if ";" in tokenList[i:]:
			nextSemicolonIndex = i+1 + tokenList[i+1:].index(";")
		elif tokenList[i] in ("#define", "#pragma"):
			# A Compiler directive like #define statement does not necessarily end with a semicolon
			pass
		elif checkIfFunctionDefinition(tokenList[i:])[0] == True:
			pass
		else:
			errorMessage = "ERROR - every non-#define C variable declaration must end with a semicolon - the current segment <%s> doesn't - hence exiting"%(STR(list2string(tokenList[i:])))
			errorRoutine(errorMessage)
			PRINT ("ERROR in parseCodeSnippet()" )
			return False
#			sys.exit()
			
		# The first token in evey declaration segment must be an enum (definition/declaration), a struct ir union, a typedef, or another typedeffed struct/union
		# Actually, one quark of C is that typedef can be anywhere. For example, this is a valid declaration: long unsigned typedef int long ullong; 
		
		# Let's try some conversions:
		
		# typedef int * prtArrayInt[5][6];	prtArrayInt (*funcPtr)(int, char);	==>	int * ((*funcPtr)(int, char))[5][6]
		
		#################################
		####     T Y P E D E F       ####
		#################################
		
		if tokenList[i] == "typedef":
			PRINT ("Found typedef" )
			# There must be at least two token before the semi-colon
			if nextSemicolonIndex <= i + 2:
				errorMessage = "ERROR - Illegal statement formation (semicolon without adequate typedef variable type and name) - exiting"
				errorRoutine(errorMessage)
				PRINT ("ERROR in parseCodeSnippet() - nextSemicolonIndex =",nextSemicolonIndex,"tokenList[i:] = tokenList[",i,":]=",tokenList[i:] )
				return False
				sys.exit()
				
			# There are two kinds of typedef - typedef on a struct/union/enum, and another on regular variables.
			if tokenList[i+1] == "struct" or tokenList[i+1] == "union" or tokenList[i+1] == "enum":
				i = i + 1	# We still need to process the struct
				continue # Go to the next iteration of the while loop so that we can take care of the struct/union/enum
			else:	# Regular typedef
				# This works only for very simple #define-like typedefs
				newDatatypeName = tokenList[nextSemicolonIndex-1]
				newDatatypeMeaning = tokenList[i+1:nextSemicolonIndex-1]
				if newDatatypeName in getDictKeyList(typedefs):
					PRINT ("ERROR in parseCodeSnippet()" )
					errorMessage = "typedef %s already exists!"%(newDatatypeName)
					errorRoutine(errorMessage)
					return False
					sys.exit()
				else:
					PRINT ("Will add in future", newDatatypeName, "which means <", newDatatypeMeaning, "> to the typedefs dictionary" )
					# We are now doing typedef as part of regular variable declaration resolution later - so commenting here
#					typedefs[newDatatypeName] = newDatatypeMeaning
					PRINT ("After non-addition, typedefs dictionary = ",typedefs )
					i = i + 1	# We still need to process the regular variable declaration
					continue # Go to the next iteration of the while loop so that we can take care of the variable declaration
				
			# Think right now this is redundant ....
			i = nextSemicolonIndex+1
			continue
		
		
		#################################
		####     __attribute__       ####
		#################################
		elif tokenList[i] == ATTRIBUTE_STRING:
			parseAttributeResult = parseAttribute(tokenList[i:])
			if parseAttributeResult[0] != True:
				errorMessage = "ERROR in parseCodeSnippet() after calling parseAttribute()"
				errorRoutine(errorMessage)
				return False
			else:
				d = parseAttributeResult[1]["distance"]
				i = i+1+d+1
		
		
		###########################
		####   P R A G M A     ####
		###########################

		# Currently it only supports #prgama(push), #prgama(pop), and #prgama(some value)
		elif tokenList[i] == "#pragma":
			if tokenList[i+1] == "pack":
				if tokenList[i+2] != "(":
					errorMessage = "ERROR in parseCodeSnippet() - must supply the parenthesized alignment value after a #pragma pack statement - no beginning parenthesis"
					errorRoutine(errorMessage)
					return False
				elif ")" not in tokenList[i+3:]:
					errorMessage = "ERROR in parseCodeSnippet() - must supply the parenthesized alignment value after a #pragma pack statement - no ending parenthesis"
					errorRoutine(errorMessage)
					return False
				else:
					nextFirstBraceBeginIndex = i+2
					nextFirstBraceEndIndex = nextFirstBraceBeginIndex + matchingBraceDistance(tokenList[nextFirstBraceBeginIndex:])
					if nextFirstBraceEndIndex == nextFirstBraceBeginIndex + 1:		#pragma pack()     /* restore compiler's default alignment setting */
						pragmaPackCurrentValue = pragmaPackDefaultValue
					else:
						parseArgumentListResult = parseArgumentList(tokenList[nextFirstBraceBeginIndex:nextFirstBraceEndIndex+1])
						if parseArgumentListResult == False:
							errorMessage = "ERROR in parseCodeSnippet() - error calling parseArgumentList(%s)"%STR(tokenList[nextFirstBraceBeginIndex:nextFirstBraceEndIndex+1])
							errorRoutine(errorMessage)
							return False
						else:
							for item in parseArgumentListResult:
								PRINT("Currently handling #pragma pack(",item,")")
								if item == "push":
									if pragmaPackCurrentValue != None:
										pragmaPackStack.append(pragmaPackCurrentValue)
								elif item == "pop":
									if not pragmaPackStack:
										errorMessage = "ERROR in parseCodeSnippet() - cannot pop from the #pragma stack since it is empty"
										errorRoutine(errorMessage)
										return False
									else:
										pragmaPackCurrentValue = pragmaPackStack.pop()
								else:
									parseArithmeticExpressionResult = parseArithmeticExpression(item)
									if parseArithmeticExpressionResult == False:
										errorMessage = "ERROR in parseCodeSnippet() - error calling parseArithmeticExpression(parenthesized alignment value of = <%s> after a #pragma pack (%s) statement - no beginning parenthesis"%(STR(item), STR(parseArithmeticExpressionResult))
										errorRoutine(errorMessage)
										return False
									else:
										evaluateArithmeticExpressionResult = evaluateArithmeticExpression(parseArithmeticExpressionResult)
										if evaluateArithmeticExpressionResult[0] != True:
											errorMessage = "ERROR in parseCodeSnippet() - error calling evaluateArithmeticExpression(AST = <%s>) after a #pragma pack statement"%(STR(parseArithmeticExpressionResult))
											errorRoutine(errorMessage)
											return False
										else:
											result = evaluateArithmeticExpressionResult[1]
											if not checkIfIntegral(result):
												errorMessage = "ERROR in parseCodeSnippet() - output (%s) from evaluateArithmeticExpression() after a #pragma pack statement is not integral"%(STR(result))
												errorRoutine(errorMessage)
												return False
											elif result < 1:
												errorMessage = "ERROR in parseCodeSnippet() - output (%s) from evaluateArithmeticExpression() after a #pragma pack statement must be at least 1"%(STR(result))
												errorRoutine(errorMessage)
												return False
											elif result not in (1,2,4,8, 16):
												errorMessage = "ERROR in parseCodeSnippet() - output (%s) from evaluateArithmeticExpression() after a #pragma pack statement must be 1,2 4 8 or 16"%(STR(result))
												errorRoutine(errorMessage)
												return False
											else:
												pragmaPackCurrentValue = result
												PRINT("Assigned the result =",result,"to the pragmaPackCurrentValue, while the content of current pragmaPackStack is",pragmaPackStack)
											i = nextFirstBraceEndIndex+1
		
		###########################
		####     E N U M       ####
		###########################
		
		elif tokenList[i] == "enum":
			parseEnumResult = parseEnum(tokenList, i)
			if parseEnumResult == None:
				errorMessage = "Error coding parseEnum() - return value is None"
				errorRoutine(errorMessage)
				return False
			elif parseEnumResult == False:
				errorMessage = "Error calling parseEnum()"
				errorRoutine(errorMessage)
				return False
			else:
				i = parseEnumResult
		
		
			
				
				
		###########################################
		####     P R E P R O C E S S O R       ####
		###########################################
		
		elif tokenList[i] in preprocessingDirectives:
			
			resultPair = fistAndLastTokenIndicesOnSameLineForTokenNumber(i, tokenListInformation)
			if resultPair == False:
				errorMessage = "ERROR in parseCodeSnippet() after trying to find the first and last tokens for tokenList["+STR(i)+"] = "+tokenList[i]
				errorRoutine(errorMessage)
				return False
			else:
				i = resultPair[1] + 1	# Move the pointer
				continue


		#################################################################
		####     S T R U C T / U N I O N   DEFINTION / DECLARATION	 ####
		#################################################################

		elif (tokenList[i] in ("struct","union")):
			structOrUnionType = tokenList[i]
			usingDummyVariable = False
			memberDeclarationStatementStartIndex = None
			typedefStatement = False
			structDefinitionStartIndex = i
			if ';' not in tokenList[i+1:]:
				errorMessage = "ERROR in parseCodeSnippet(): No semicolon at the end"
				errorRoutine(errorMessage)
				return False
			else:
				nextSemicolonIndex = i+1 + tokenList[i+1:].index(";")
				
				variableDeclarationStartIndex = i
				while (variableDeclarationStartIndex > 0):
					if tokenList[variableDeclarationStartIndex-1] in [ 'auto','register','static','extern', 'const','volatile', 'typedef']:
						if tokenList[variableDeclarationStartIndex-1] == 'typedef':
							typedefStatement = True
						variableDeclarationStartIndex = variableDeclarationStartIndex - 1
					else:
						break

				structDefinedHere = False
				
				# Struct Definition (and optionally declaration too, if there are variables there)
				if '{' in tokenList[i+1:nextSemicolonIndex]:
					curlyBraceStartIndex = i+1 + tokenList[i+1:].index("{")
					if '}' in tokenList[curlyBraceStartIndex+1:]:
						matchingBraceDistanceResult = matchingBraceDistance(tokenList[curlyBraceStartIndex:])
						if matchingBraceDistanceResult <= 0:
							errorMessage = "ERROR in parseCodeSnippet(): The supplied tokenList has an illegal matchingBraceDistanceResult =" + STR(matchingBraceDistanceResult)
							errorRoutine(errorMessage)
							return False
						else:
							structDefinedHere = True
							# A struct will have a lexical scope of variables in it. This is the first 
							scopeStartVariableId = totalVariableCount
							curlyBraceEndIndex = curlyBraceStartIndex + matchingBraceDistance(tokenList[curlyBraceStartIndex:])
							if ';' in tokenList[curlyBraceEndIndex+1:]:
								nextSemicolonIndex = curlyBraceEndIndex+1 + tokenList[curlyBraceEndIndex+1:].index(";")
							else:
								errorMessage = "Error coding parseStructure() - Missing semicolon at the end after }"
								errorRoutine(errorMessage)
								return False
							# The result is actually the structure name (comes handy for anonymous structures)
							level = 0
							parseStructureResult = parseStructure(tokenList, curlyBraceStartIndex,"--Global--", level)
							if parseStructureResult == None:
								errorMessage = "Error coding parseStructure() - return value is None"
								errorRoutine(errorMessage)
								return False
							elif parseStructureResult == False:
								errorMessage = "Error calling parseStructure() from parseCodeSnippet() - return Value is False"
								errorRoutine(errorMessage)
								return False
								
							# There might be __attribute__(( ... )) statements after this
							
							lastItemConsumedIndex = curlyBraceEndIndex
							while tokenList[lastItemConsumedIndex+1] == ATTRIBUTE_STRING:
								parseAttributeResult = parseAttribute(tokenList[lastItemConsumedIndex+1:])
								if parseAttributeResult[0] != True:
									errorMessage = "ERROR in parseCodeSnippet() after calling parseAttribute() post struct definition handling"
									errorRoutine(errorMessage)
									return False
								else:
									d = parseAttributeResult[1]["distance"]
									lastItemConsumedIndex = lastItemConsumedIndex+2+d
								
							
							# A struct will have a lexical scope of variables in it.
							scopeEndVariableId = totalVariableCount - 1
							
							if tokenList[lastItemConsumedIndex+1] == ';':	# Only defnition, no declaration
#							if tokenList[curlyBraceEndIndex+1] == ';':	# Only defnition, no declaration
								structName = parseStructureResult
								PRINT ("Processed struct/union ",parseStructureResult,"(only definition, no declared struct/union variables). Nothing more to do" )
								numFakeEntries = i - variableDeclarationStartIndex
								memberDeclarationStatementStartIndex = variableDeclarationStartIndex
								memberDeclarationStatement = tokenList[variableDeclarationStartIndex:curlyBraceStartIndex]
								if memberDeclarationStatement[-1] != structName:	# Append the structure name for Anonymous structures
									memberDeclarationStatement.append(structName)
								usingDummyVariable = True
								dummyVariableCount += 1
								dummyVariableName = dummyVariableNamePrefix + STR(dummyVariableCount)
								memberDeclarationStatement.append(dummyVariableName)
								memberDeclarationStatement.append(';')	# Put back the semicolon
#								i = curlyBraceEndIndex+2
								i = lastItemConsumedIndex+2
#								continue
							else:	# Some variable(s) declared after the struct definition
								structName = parseStructureResult
								# Now process declarations. Create a fake declaration statement as if
#								if structDefinitionStartIndex>0 and tokenList[structDefinitionStartIndex-1] == "typedef":
								if structDefinitionStartIndex != variableDeclarationStartIndex:
#									memberDeclarationStatement = [tokenList[structDefinitionStartIndex-1],tokenList[structDefinitionStartIndex], structName]
									memberDeclarationStatement = tokenList[variableDeclarationStartIndex: structDefinitionStartIndex+1] +[structName]
									numFakeEntries = structDefinitionStartIndex-variableDeclarationStartIndex + 1
#									memberDeclarationStatementStartIndex = structDefinitionStartIndex-1
									memberDeclarationStatementStartIndex = variableDeclarationStartIndex
								else:
									memberDeclarationStatement = [tokenList[structDefinitionStartIndex], structName]
									numFakeEntries = 1
									memberDeclarationStatementStartIndex = structDefinitionStartIndex
#								memberDeclarationStatement.extend(tokenList[curlyBraceEndIndex+1:nextSemicolonIndex+1])
								memberDeclarationStatement.extend(tokenList[lastItemConsumedIndex+1:nextSemicolonIndex+1])
#								i = curlyBraceEndIndex	# Now i points to the just before actual structure variables that are declared
								i = lastItemConsumedIndex	# Now i points to the just before actual structure variables that are declared
								PRINT("memberDeclarationStatement = ",memberDeclarationStatement)
								
					else:
						errorMessage = "ERROR in parseCodeSnippet(): No matching }"
						errorRoutine(errorMessage)
						return False
						
				else:	# Regular struct declaration (no definition)
					PRINT ("Regular struct declaration (no definition), i=",i)
					if structDefinitionStartIndex>0 and tokenList[structDefinitionStartIndex-1]=="typedef":
						memberDeclarationStatementStartIndex = structDefinitionStartIndex - 1
					else:
						memberDeclarationStatementStartIndex = structDefinitionStartIndex
					structName = tokenList[structDefinitionStartIndex+1]
					
					
					memberDeclarationStatement = tokenList[memberDeclarationStatementStartIndex:nextSemicolonIndex+1]
					numFakeEntries = 0
#					i = structDefinitionStartIndex	# It assumes that this statement will be this format: struct structName variables;
					i = memberDeclarationStatementStartIndex	# It assumes that this statement will be this format: [typedef] struct structName variables;
					
				# Now parse all the member variables individually
				PRINT ("Going to parse from tokenList[memberDeclarationStatementStartIndex=",memberDeclarationStatementStartIndex,"through nextSemicolonIndex=",nextSemicolonIndex,"] (both indices included, possibly also typedef) = ",memberDeclarationStatement )
				parsed5tupleList = parseVariableDeclaration(memberDeclarationStatement)
				if parsed5tupleList == False:
					errorMessage = "ERROR in parseCodeSnippet() for struct after calling parseVariableDeclaration(memberDeclarationStatement) for memberDeclarationStatement ="+ STR(memberDeclarationStatement) 
					errorRoutine(errorMessage)
					return False
				PRINT ("struct declaration",parsed5tupleList, "parsed" )
				
				variableFoundWithDataOverlapWithStructMembers = False
				
				for item in parsed5tupleList:
					PRINT ("struct ",structName,"has the following declarations after it" )
					PRINT ("Main variable name is ",item[0],"of size",item[1],"and it is located at relative index of ",item[3],"inside the variable declaration statement",item[2] )
					# Each member of the list follows exactly the same format as the parsed5tupleList, with one key addition - the 6th item.
					# This 6th member now represents the absolute index (within the tokenList) of the variable name.
					if not structDefinedHere and not usingDummyVariable and tokenList[i+item[3]-numFakeEntries]!=item[0]:
						OUTPUT ("ERROR in parseCodeSnippet() - for i=",i,"tokenList[i+item[3]-numFakeEntries] = tokenList[",i,"+",item[3],"-",numFakeEntries,"] =",tokenList[i+item[3]-numFakeEntries],"!=item[0]=",item[0] )
						errorMessage = "ERROR in parseCodeSnippet() for struct as location of struct variable does not match for i="+STR(i)+" and tokenList[i]=<"+STR(tokenList[i])+">, memberDeclarationStatement="+ STR(memberDeclarationStatement) 
						errorRoutine(errorMessage)
						return False
					else:
						if not structDefinedHere and not usingDummyVariable:
							PRINT ("In parseCodeSnippet(), - for i=",i,"tokenList[i+item[3]-numFakeEntries] = tokenList[",i,"+",item[3],"-",numFakeEntries,"] =",tokenList[i+item[3]-numFakeEntries],"matches item[0]=",item[0] )
						globalTokenListIndex = i+item[3]-numFakeEntries if not usingDummyVariable else curlyBraceEndIndex+1
						variableName = item[0]
						variableSize = item[1]
						variableId = totalVariableCount
						variableDeclarationStatement = item[2]
						variableNameIndex = item[3]
						variableDescriptionExtended = item[4]
						variableDescriptionExtended["globalTokenListIndex"] = globalTokenListIndex
						variableDescriptionExtended["level"] = 0
						variableDescriptionExtended["variableId"] = variableId
						variableDescriptionExtended["DataOverlapWithStructMembers"] = True if not variableFoundWithDataOverlapWithStructMembers and structDefinedHere and variableDescriptionExtended["datatype"] == structName else False
						item2add = [variableName,variableSize,variableDeclarationStatement,variableNameIndex,variableDescriptionExtended]
						variableDeclarations.append(item2add) 
						totalVariableCount += 1

					if structDefinedHere and variableDescriptionExtended["datatype"] == structName and variableFoundWithDataOverlapWithStructMembers == False:
						variableFoundWithDataOverlapWithStructMembers = True
						globalScopes.append([variableId, scopeStartVariableId, scopeEndVariableId])
					else:
						globalScopes.append([variableId, variableId, variableId])

					if memberDeclarationStatementStartIndex == None:
						errorMessage = "ERROR in parseCodeSnippet() memberDeclarationStatementStartIndex not populated for i="+STR(i)+" and tokenList[i]=<"+STR(tokenList[i])+">, memberDeclarationStatement="+ STR(memberDeclarationStatement) 
						errorRoutine(errorMessage)
						return False
						
				i = nextSemicolonIndex+1



		elif tokenList[i] in [ 'auto','register','static','extern', 'const','volatile']:
			#	storageClassSpecifier = [ 'auto','register','static','extern','typedef']
			#	typeQualifier = ['const','volatile']
			i = i+1
				
		###############################################################################################################################
		####     D E R I V E D  ( T Y P E D E F)   T Y P E   A N D    O T H E R    V A R I A B L E     D E C L A R A T I O N S     ####
		###############################################################################################################################
				

		# regular declaration statements without any enclosing structures
		elif (tokenList[i] in declarationKeywords) or (tokenList[i] in getDictKeyList(typedefs)) or (tokenList[i] in getDictKeyList(typedefsBuiltin)):
			caseOfUndefinedBuiltinTypedef = False 	# Default value
			functionCheckResult = checkIfFunctionDefinition(tokenList[i:])
			if functionCheckResult[0]==False and ";" not in tokenList[i:]:
				PRINT ("No semicolon in tokenList[i:] = tokenList[",i,":] = ",tokenList[i:] )
				errorMessage = "ERROR in parseCodeSnippet() while checking for derived types - every variable declaration must end with a semicolon - exiting"
				errorRoutine(errorMessage)
				return False
#				sys.exit()
			declarationEndIndex = len(tokenList[i:])
			if ';' in tokenList[i:]:
				nextSemicolonIndex = i+1 + tokenList[i+1:].index(";")
				declarationEndIndex = nextSemicolonIndex
			if functionCheckResult[0]==True:
				functionDeclarationEndIndex = functionCheckResult[1]
				declarationEndIndex = functionDeclarationEndIndex if functionDeclarationEndIndex < declarationEndIndex else declarationEndIndex
				
			PRINT ("Current tokenList = ",tokenList,"i=",i )
			typedefStatement = False
			variableDeclarationStartIndex = i
			while (variableDeclarationStartIndex > 0):
				if tokenList[variableDeclarationStartIndex-1] in [ 'auto','register','static','extern', 'const','volatile', 'typedef']:
					if tokenList[variableDeclarationStartIndex-1] == 'typedef':
						typedefStatement = True
					variableDeclarationStartIndex = variableDeclarationStartIndex - 1
				else:
					break
			
#			variableDeclarationStartIndex = i-1 if (i>0 and tokenList[i-1]=="typedef") else i
			memberDeclarationStatement = tokenList[variableDeclarationStartIndex:declarationEndIndex+1]
			PRINT ("Going to parse from  tokenList[",variableDeclarationStartIndex,"through",declarationEndIndex,"] (both indices included) = ",memberDeclarationStatement )

			# The user forgot to explicitly declare the typedef
			if (tokenList[i] in getDictKeyList(typedefsBuiltin)) and (tokenList[i] not in getDictKeyList(typedefs)):
				caseOfUndefinedBuiltinTypedef = True
				list2parse = typedefsBuiltin[tokenList[i]]
				PRINT ("Going to add",tokenList[i],"to the typedefs, whose type definition would be", list2parse)
				parsed5tupleList = parseVariableDeclaration(list2parse)
			
			elif tokenList[i] not in getDictKeyList(typedefs):
				list2parse = memberDeclarationStatement
				parsed5tupleList = parseVariableDeclaration(list2parse)
			else:
			
				list2parse = convertDerivedTypeDeclarationIntoBaseTypeDeclaration(tokenList,i)
				if list2parse == False:
					errorMessage = "ERROR in parseCodeSnippet() - error encountered in convertDerivedTypeDeclarationIntoBaseTypeDeclaration() while trying to convert the Derived type"
					errorRoutine(errorMessage)
					return False
				else:
					parsed5tupleList = parseVariableDeclaration(list2parse)			
				
				
			if parsed5tupleList == False:
				errorMessage = "ERROR in parseCodeSnippet() after calling parseVariableDeclaration(list2parse) for list2parse = "+ STR(list2parse)
				errorRoutine(errorMessage)
				return False
			
			PRINT ("Non-struct declaration",parsed5tupleList, "parsed" )
			for item in parsed5tupleList:
				typeSpecifierEndIndex = item[4]["typeSpecifierEndIndex"]
				variableDeclarationStatement = item[2]
				PRINT ("Main variable name is ",item[0],"of size",item[1],"and it is located at relative index of ",item[3],"inside the variable declaration statement",item[2],", where the base type specifier ends at index =", )
				if tokenList[i] in getDictKeyList(typedefs):
					PRINT ("We modified the declaration statement, so we know that position index of the declared variable", item[0],"would not match (hence not checking it)" )
					variableNameIndex = memberDeclarationStatement.index(item[0])
				elif tokenList[variableDeclarationStartIndex+item[3]]!=item[0]:
					errorMessage = "ERROR in parseCodeSnippet() - for variableDeclarationStartIndex = "+ STR(variableDeclarationStartIndex) + " tokenList[variableDeclarationStartIndex+item[3]] = " + STR(tokenList[variableDeclarationStartIndex+item[3]]) + " !=item[0]=" + STR(item[0])
					errorRoutine(errorMessage)
					return False
				else:
					variableNameIndex = item[3]
				
				# If this is a function definition (not declaration), do not add it to the variableDeclarations or globalScopes
				if item[4]["datatype"].startswith("function") and item[4]['isInitialized']== True:
					PRINT("Omitting function",item[0],"since it is a function defintion, not a declaration")
					continue
					
				variableId = totalVariableCount
				globalTokenListIndex = variableDeclarationStartIndex+variableNameIndex
				variableDescriptionExtended = item[4]
				variableDescriptionExtended["globalTokenListIndex"]=globalTokenListIndex if not caseOfUndefinedBuiltinTypedef else -10000
				variableDescriptionExtended["level"] = 0
				variableDescriptionExtended["variableId"] = variableId
				variableDescriptionExtended["DataOverlapWithStructMembers"] = False
				totalVariableCount += 1
				variableDeclarations.append([item[0],item[1],item[2],variableNameIndex,variableDescriptionExtended])
				
				globalScopes.append([variableId, variableId, variableId])
				
				# Handle the Typedefs
				if i>0 and tokenList[i-1]=="typedef" and "typedef" not in variableDeclarationStatement[:typeSpecifierEndIndex+1]:
					errorMessage = "CODING ERROR: no \"typedef\" in variableDeclarationStatement[:typeSpecifierEndIndex+1] =" + STR(variableDeclarationStatement[:typeSpecifierEndIndex+1])
					errorRoutine(errorMessage)
					sys.exit()

			if caseOfUndefinedBuiltinTypedef:
				# In this cycle we will just add the builtin typedef to typedef and update variableDeclarations accordingly. In the next cycle, we will reprocess this.
				continue
			else:
				i = declarationEndIndex + 1


		##########################################################
		####     N O N - D E C L A R A T I O N    C O D E     ####
		##########################################################
						
		# This is the place where all non-declaration or non-defintion code should come
		else:
			PRINT("We have encoutered non-declared code",tokenList[i:])
			result = parseRegularNonDeclarationCode(tokenList[i:])
			PRINT("result =",result)
			if result[0] == False:
				errorMessage = "ERROR in parseCodeSnippet() - cannot parse tokenList" + STR(tokenList[i:])
				errorRoutine(errorMessage)
				return False
			else:
				i = i+result[1]+1	# Recall that parseRegularNonDeclarationCode is relative to the first item index, starting from 0
				
	
		continue

	
	PRINT ("\n==============================================\nvariableDeclarations =" )
	for item in variableDeclarations: 
		PRINT (item)
	PRINT ("\n=====================================================\n" )
	PRINT ("typedefs = ",typedefs )
#	sys.exit()

	return True


#str = "3+ -1"
#lst = parseArithmeticExpression(tokenizeLines(str))
#PRINT ("str =",str,"lst =",lst )
#sys.exit()

#str1 = "(int)c"
#parsed = parseArithmeticExpression(tokenizeLines(str1))
#PRINT ("string <",str1,"> parses into", parsed )
#valid = isASTvalid(parsed)
#PRINT ("whose validity = ",valid )
#sys.exit()

			

#######################################################################################
#
# 	The Main Working Module
#
#######################################################################################

def mainWork():	
#	global PRINT_DEBUG_MSG		# MannaManna
	global lines, tokenLocationLinesChars

	# Pre-process (remove comment etc.)
	
	PRINT ("Before calling preProcess()" )
#	PRINT_DEBUG_MSG = True		# MannaManna
	preProcessResult = preProcess()
	if preProcessResult == False:
		OUTPUT ("ERROR in mainWork after calling preProcess()" )
		return False
	PRINT ("After calling preProcess()" )
#	PRINT_DEBUG_MSG = False		# MannaManna
	
	# Tokenize and resolve macros
	
	PRINT ("Before calling tokenizeLines(lines)" )
	tokenListResult = tokenizeLines(lines)
	if tokenListResult == False:
		OUTPUT ("ERROR inside mainWork() after calling tokenizeLines(lines) for lines =", lines )
		return False
	else:
		tokenList = tokenListResult[0]
		
	PRINT ("After calling tokenizeLines(lines)" )
	PRINT ("tokenList =",tokenList )
	PRINT ("lines =",lines )
	PRINT ("Before calling tokenLocations(lines, tokenList)" )
	
	# Note down the token locations (not relevant for batch mode)
	
	tokenLocationLinesChars = tokenLocations(lines, tokenList)
	if tokenLocationLinesChars == False:
		OUTPUT ("ERROR in mainWork() after calling tokenLocations(lines, tokenList) for lines=",lines," and tokenList =",tokenList )
		return False
	PRINT ("After calling tokenLocations, the starting <line,char> and ending <line,char> for each token is", tokenLocationLinesChars )
	rootNode = Node(tokenList, "rootNode");
	
	# Parse the Code snippets
	
	PRINT ("Before calling parseCodeSnippet(tokenList, rootNode)" )
	parseCodeSnippetOutput = parseCodeSnippet(tokenListResult, rootNode) 
	if parseCodeSnippetOutput == False:
		OUTPUT ("ERROR after calling parseCodeSnippet(tokenList, rootNode)" )
		return False
	PRINT ("After calling parseCodeSnippet(tokenList, rootNode)" )
	PRINT ("\n\nNow traversing the AST ...\n\n" )
	rootNode.traverse()
	
	return True
	

def checkIfValidRawInput(inputBytes):
	if PYTHON2x and (not isinstance(inputBytes,basestring)):
		PRINT ("ERROR: Inside checkIfValidRawInput(), input byte stream <",inputBytes,"> is not a valid bytestream input - its type is", type(inputBytes),"instead of \"bytes\"")
		return False
	elif PYTHON3x and (not isinstance(inputBytes,(bytes,bytearray))):
		PRINT ("ERROR: Inside checkIfValidRawInput(), input byte stream <",inputBytes,"> is not a valid bytestream input - its type is", type(inputBytes),"instead of \"bytes\"")
		return False
	else:
		return True
		
###################################################################################################################################
# The different data types (like integer, float, double etc.) are stored differently. Here is how to decipher the stored value.
###################################################################################################################################

def printHexStringWord (inputBytes):
	if not checkIfValidRawInput(inputBytes):
		PRINT ("ERROR: Inside printHexStringWord(), input byte stream <",inputBytes,"> is not a valid bytestream input" )
		return False
	else:
		returnString="<"
		for byte in inputBytes:
			returnString += "%02X"%ORD(byte)
		returnString += ">"
		return returnString
	'''
	if len(inputBytes) == 1:
		return "<%02X>" %(ord(inputBytes[0]))
	elif len(inputBytes) == 2:
		return "<%02X %02X>" %(ord(inputBytes[0]),ord(inputBytes[1]))
	elif len(inputBytes) == 4:
		return "<%02X %02X %02X %02X>" %(ord(inputBytes[0]),ord(inputBytes[1]),ord(inputBytes[2]),ord(inputBytes[3]))
	elif len(inputBytes) == 8:
		return "<%02X %02X %02X %02X %02X %02X %02X %02X>" %(ord(inputBytes[0]),ord(inputBytes[1]),ord(inputBytes[2]),ord(inputBytes[3]),
															 ord(inputBytes[4]),ord(inputBytes[5]),ord(inputBytes[6]),ord(inputBytes[7]))
	else:
		return False
	'''


def calculateInternalValue(inputBytes, littleEndianOrBigEndian=LITTLE_ENDIAN, datatype="int", signedOrUnsigned="signed", bitFieldSize=0, bitStartPosition=0):

	if littleEndianOrBigEndian not in (LITTLE_ENDIAN, BIG_ENDIAN):
		PRINT ("ERROR: Inside calculateInternalValue(), littleEndianOrBigEndian = ",littleEndianOrBigEndian,"is NOT either Little-Endian or Big-Endian" )
		return False
	elif littleEndianOrBigEndian == LITTLE_ENDIAN:
		inputFormat = "Little-Endian"
	elif littleEndianOrBigEndian == BIG_ENDIAN:
		inputFormat = "Big-Endian"
	else:
		sys.exit()
		

	# In Little-Endian, the bits are packed from the LSB to MSB. So, if we have four bitfields in an integer, each 8 bits wide, they will be packed like this:
	#      Bit #   MSb  31........24 23 ........16 15 ........8 7...........0 LBb
	#                   N7........N0 M7.........M0 L7........L0 K7.........K0
	#
	# When our program analyzes the structure, it will come up with the following bitStartPosition values:
	# 
	#   struct {
	#             K : 8;	// bitStartPosition = 0
	#			  L : 8;    // bitStartPosition = 8
	#			  M : 8;    // bitStartPosition = 16
	#			  N : 8;    // bitStartPosition = 24
	#   }
	# But, this is different than the usual way of Little endian packing. For example, if the little-endian integer had an interanl 0xNMLK value, in the displayed byte
	# it shows as 0xKLMN (the order of the byte gets flipped). Similarly, 
	# In Big-Endian, the bits are packed from the MSB to LSB. So, change the starting position accordingly.
	#
	if littleEndianOrBigEndian == BIG_ENDIAN:
		origBitStartPosition = bitStartPosition
		bitStartPosition = primitiveDatatypeLength[datatype]*BITS_IN_BYTE - bitFieldSize - bitStartPosition if bitFieldSize > 0 else bitStartPosition
		PRINT ("Inside calculateInternalValue() for inputFormat=",inputFormat, "for datatype of ",datatype,", changed the bitStartPosition from ",origBitStartPosition,"to",bitStartPosition,"for bitFieldSize =",bitFieldSize)
	
	PRINT ("\nInside calculateInternalValue(inputBytes =",printHexStringWord(inputBytes),"inputFormat =",inputFormat, "datatype =",datatype, "signedOrUnsigned =",signedOrUnsigned, "bitFieldSize =",bitFieldSize, "bitStartPosition = ",bitStartPosition)
	
	if datatype not in getDictKeyList(primitiveDatatypeLength):
		PRINT ("ERROR: Inside calculateInternalValue(), datatype ",datatype,"NOT found in primitiveDatatypeLength.keys()=",getDictKeyList(primitiveDatatypeLength) )
		return False
#	elif not checkIfString(inputBytes):
	elif not checkIfValidRawInput(inputBytes):
		PRINT ("ERROR: Inside calculateInternalValue(), input byte stream ",printHexStringWord(inputBytes)," is not a valid input" )
		return False
	elif not inputBytes:
		PRINT ("ERROR: Inside calculateInternalValue(), input byte stream <",inputBytes,"> of length",len(inputBytes),"Hex ",printHexStringWord(inputBytes)," is not a valid input (most likely empty)" )
		return False
	elif signedOrUnsigned!="unsigned" and signedOrUnsigned!="signed" :
		PRINT ("ERROR: Inside calculateInternalValue(), input byte stream ",printHexStringWord(inputBytes)," is not a valid input - the input", signedOrUnsigned, "value is not either signed or unsigned" )
		return False
	elif bitFieldSize > 0 and bitFieldSize > primitiveDatatypeLength[datatype]*BITS_IN_BYTE:	# It is a bitfield, so the MSBit is dependent on the bit field size
		PRINT ("ERROR: Inside calculateInternalValue(), Width of bitfield", bitFieldSize, "exceeds its type (",datatype,")" )
		return False
	elif bitFieldSize > 0 and (bitStartPosition <0 or bitStartPosition >= primitiveDatatypeLength[datatype]*BITS_IN_BYTE):
		PRINT ("ERROR: Inside calculateInternalValue(), For the",bitFieldSize,"-bit-wide",datatype,", the bitfield starting position", bitStartPosition, "is outside the valid range of <0,",primitiveDatatypeLength[datatype]*BITS_IN_BYTE-1,">" )
		return False
	elif bitStartPosition !=0 and bitFieldSize <= 0:
		PRINT ("ERROR: Non-bit fields cannot have a the bitfield starting position", bitStartPosition)
		return False
	elif bitFieldSize>0 and bitStartPosition+bitFieldSize > primitiveDatatypeLength[datatype]*BITS_IN_BYTE:
		PRINT ("ERROR: Inside calculateInternalValue(), for field width of", bitFieldSize," bits of",datatype,", the bitfield starting position", bitStartPosition, "is outside the valid range of <0,",primitiveDatatypeLength[datatype]*BITS_IN_BYTE-bitFieldSize,">" )
		return False
	elif len(inputBytes) not in (1,2,4,8):
		PRINT ("WARNING: Inside calculateInternalValue(), length of inputBytes is not 1,2, 4 or 8 - Endianness is immaterial" )
		return False
	else:
#		PRINT ("="*30,"\nNo obvious input error!\n","="*30 )
		
		# This is the value without considering the sign
		IEEEFormatValue = 0
		for i in range(len(inputBytes)):
			if littleEndianOrBigEndian == BIG_ENDIAN:
				IEEEFormatValue = IEEEFormatValue + ORD(inputBytes[i])*2**((len(inputBytes)-i-1)*BITS_IN_BYTE)
			elif littleEndianOrBigEndian == LITTLE_ENDIAN:
				IEEEFormatValue = IEEEFormatValue + ORD(inputBytes[i])*2**(i*BITS_IN_BYTE)
			else:
				sys.exit()
		PRINT ("For inputBytes =",printHexStringWord(inputBytes), "the IEEEFormatValue =",IEEEFormatValue,"(basically 0x%x"%(IEEEFormatValue),")" )

		################################################################
		# Pointer
		################################################################
		if datatype == "pointer":
			returnValue = IEEEFormatValue
		
		#######################################################################
		# Float / Double precision (all float/double are automatically signed)
		#######################################################################
		
		elif datatype in ("float","double"):	#For float, 31-st bit is Sign, [30:23] is 8-bit biased Exponent, [22:0] is 23-bit Mantissa
			if (datatype == "float" and len(inputBytes) != 4) or (datatype == "double" and len(inputBytes) != 8) :
				PRINT ("ERROR: Inside calculateInternalValue(), input byte stream ",printHexStringWord(inputBytes)," is not a valid float/double input" )
				return False
			else:
				fieldSize = 32 if datatype == "float" else 64
				exponentSize = 8 if datatype == "float" else 11
				mantissaSize = fieldSize - 1 - exponentSize
				exponentMask = ((1<<exponentSize)-1)<<mantissaSize
				mantissaMask = (1<<mantissaSize)-1
				exponentBias = (1<<(exponentSize-1))-1
				sign =  IEEEFormatValue >> (fieldSize-1)
				biasedExponent = (IEEEFormatValue & exponentMask) >> mantissaSize
				unbiasedExponent = biasedExponent - exponentBias
				mantissa = (IEEEFormatValue & mantissaMask)	# Recall that there is an implicit 1 at the beginning
				implicitLeadingPartOfMantissa = 1.00
				if biasedExponent == 0 or biasedExponent == (2**exponentSize) -1:
					PRINT ("WARNING: Inside calculateInternalValue(), biasedExponent = ",biasedExponent," is reserved for Special numbers" )
				if biasedExponent == 0 and mantissa == 0:
					returnValue = 0.00
				elif biasedExponent == (1<<exponentSize)-1 and mantissa == 0:
					returnValue = "+infinity" if sign == 0 else "-infinity" 
				elif biasedExponent == (1<<exponentSize)-1 and mantissa != 0:
					returnValue = "Not a Number (NaN)"
				else:
					if biasedExponent == 0 and mantissa != 0:
						PRINT ("Denormalized value (no implicit 1 in mantissa)" )
						implicitLeadingPartOfMantissa = 0
						
					mantissaWithImplicitOneincluded = "1.{:023b}".format(mantissa)
					realMantissaInDecimal = implicitLeadingPartOfMantissa + (mantissa * 1.000) / (2**mantissaSize)
					# So, the return value is (implicit.mantissa) * 2^unbiasedExponent
					returnValue = realMantissaInDecimal * (2**unbiasedExponent) * (-1 if sign == 1 else 1)
					
#				PRINT ("For inputBytes=",printHexStringWord(inputBytes),"IEEEFormatValue =",IEEEFormatValue,"sign =",sign,"biasedExponent =",biasedExponent,"exponentBias =",exponentBias,"unbiasedExponent =",unbiasedExponent )
#				PRINT ("mantissa = ",mantissa,"mantissaWithImplicitOneincluded = ",mantissaWithImplicitOneincluded, "realMantissaInDecimal = ",realMantissaInDecimal,"returnValue =",returnValue )

		################################################################
		# Signed Char/Short/Interger/Long
		################################################################
		
		elif signedOrUnsigned=="signed": 
			if datatype not in ("char", "short", "int", "long", "long long"):
				PRINT ("ERROR: Inside calculateInternalValue(), input byte stream <%s> is not a valid Signed input as the datatype = %s"%(printHexStringWord(inputBytes),datatype) )
				errorMessage = "ERROR: input byte stream <%s> is not a valid Signed input as its length = %d is not in (1,2,4 or 8)"%(printHexStringWord(inputBytes),len(inputBytes))
				errorRoutine(errorMessage)
			elif len(inputBytes) not in (1,2,4,8):
				PRINT ("ERROR: Inside calculateInternalValue(), input byte stream ",printHexStringWord(inputBytes)," is not a valid Signed input as its length =",len(inputBytes) )
				errorMessage = "ERROR: input byte stream <%s> is not a valid Signed input as its length = %d is not in (1,2,4 or 8)"%(printHexStringWord(inputBytes),len(inputBytes))
				errorRoutine(errorMessage)
				return False
			else:
				fieldWidthInBits = bitFieldSize if bitFieldSize > 0 else len(inputBytes)*8
				MSBitMask = 1 << (fieldWidthInBits-1)	# This assumes the field starts from bit 0. So, for bit-fields, you have to shift it first
				allOnesValue = (1<<fieldWidthInBits)-1		# This the 0xFF for char, or 0xFFFF for short, or 0xFFFFFFFF for int, or 0xFFFFFFFFFFFFFFFF for long
				
				# We only keep the relevant bits, and shift it to as if starting from 0. This is only useful for the bitfields
				IEEEFormatValue = (IEEEFormatValue & (allOnesValue<<bitStartPosition))>>bitStartPosition	
				
				PRINT ("For bitFieldSize=%d, bitStartPosition=%d, fieldWidthInBits=%d, MSBitMask=%x, allOnesValue=%x, IEEEFormatValue=%d" %(bitFieldSize, bitStartPosition,fieldWidthInBits,MSBitMask,allOnesValue,IEEEFormatValue) )
				
				if (IEEEFormatValue & MSBitMask) == MSBitMask: #Negative number
					# Suppose X is a positive or negative number. In two's complement system, to get -X, flip ALL the bits of X, then add one.
					# It works for both kinds of values (positive or negative) of X.
					returnValue = 0 - ((IEEEFormatValue ^ allOnesValue)+1)
				else:
					returnValue = IEEEFormatValue
					
		################################################################
		# Unsigned Char/Short/Integer/Long
		################################################################
		
		elif signedOrUnsigned=="unsigned" and datatype in ("char", "short", "short int", "int", "long", "long int", "long long"):
			if len(inputBytes) not in (1,2,4,8):
				errorMessage = "ERROR: Inside calculateInternalValue(), input byte stream "+printHexStringWord(inputBytes)+" is not a valid Signed input"
				errorRoutine(errorMessage)
				return False
			else:
				if bitFieldSize > 0:	# Only keep the relevant bits
					# Little-endian packs from LSB to MSB.   So, layout is MSb|...............|<--bitFieldSize-->|<---bitStartPosition-->| LSb
					IEEEFormatValue = (IEEEFormatValue & (( (1<<bitFieldSize)-1)<<bitStartPosition))>>bitStartPosition	
				returnValue = IEEEFormatValue
			
		################################################################
		# ERROR
		################################################################
		else:
			errorMessage = "ERROR in calculateInternalValue() - datatype <%s> is not supported -- exiting!"%datatype
			errorRoutine(errorMessage)
			return False
		
		PRINT ("datatype =",datatype)
		if DISPLAY_INTEGRAL_VALUES_IN_HEX and (datatype == "pointer" or datatype in integralDataTypes):
			return HEX(returnValue)
		else:
			return returnValue

def charIsValidHex(c):
	if ('0' <= c <= '9') or ('a' <= c <= 'f') or ('A' <= c <= 'F'):
		return True
	else:
		return False
		
# This check if the input file is really binary, or rather text representation of Hex chars. If the latter, it fills out a binary array corresponding to it.
def inputFileIsHexText():

	global binaryArray, hexCharArray 
	
	fileLengthInBytes = os.path.getsize(dataFileName)
	PRINT("Length of the",dataFileName, "file = ",fileLengthInBytes)

	with open(dataFileName, "rb") as file:
		data = file.read()
		PRINT ( "len(data) = ",len(data),"type(data)=",type(data))		# str for Python2, bytes for Python3
		#PRINT ( "type(data[0])=",type(data[0]))							# str for Python2, int for Python3
		#PRINT ( "type(data[0:1])=",type(data[0:1]))						# str for Python2, bytes for Python3

		# We cannot operate RegEx on bytes in Python3, so we need to convert it to string first. If UTF-8 complains, we know it's not text file anyway
		if PYTHON3x:
			try:
				data = data.decode("utf-8")
			except UnicodeDecodeError:
				PRINT("Input file is NOT text")
				return False
			
		#sys.exit()

	hexCharCount = 0
	spaceCount = 0
	hex0xPrefixCount = 0
	nonHexCharCount = 0
	hexCharArray = []
	binaryArray      = "" if PYTHON2x else bytearray() if PYTHON3x else []
	countItNextTime = False


	for n in range(len(data)):
		PRINT ("data[",n,"] =",data[n],"type(data[n]) =",type(data[n]))
		if re.match("[,\s]+",data[n:n+1]) and (n<len(data)-1) and re.match("[,\s]+",data[n+1:n+2]):
			continue
		elif data[n] == '0' and n<len(data)-1 and data[n+1] == 'x':	# Make sure you do not count the 0 in 0x as part of a valid Hex byte
			PRINT( "Prefix found")
			continue
		#elif countItNextTime == False and self.charIsValidHex(data[n]) and (n<len(data)-1) and self.charIsValidHex(data[n+1]):
		elif countItNextTime == False and charIsValidHex(data[n]) and (n<len(data)-1) and charIsValidHex(data[n+1]):
			countItNextTime = True
			continue
		elif re.match("[,\s]+",data[n:n+1]):
			spaceCount += 1
		#elif countItNextTime == True and self.charIsValidHex(data[n]) and (n>0) and self.charIsValidHex(data[n-1]):
		elif countItNextTime == True and charIsValidHex(data[n]) and (n>0) and charIsValidHex(data[n-1]):
			hexCharCount += 1
			hexCharArray.append(data[n-1:n+1])
			byte0 = ord(data[n-1]) - ord('0') if ('0' <= data[n-1] <= '9') else 10 + ord(data[n-1]) - ord('a') if ('a' <= data[n-1] <= 'f') else 10 + ord(data[n-1]) - ord('A') if ('A' <= data[n-1] <= 'F') else 0
			byte1 = ord(data[n  ]) - ord('0') if ('0' <= data[n  ] <= '9') else 10 + ord(data[n  ]) - ord('a') if ('a' <= data[n  ] <= 'f') else 10 + ord(data[n  ]) - ord('A') if ('A' <= data[n  ] <= 'F') else 0
			if PYTHON2x:
				binaryArray += chr(byte0*16+byte1) 
			elif PYTHON3x:
				binaryArray.append(byte0*16+byte1)
			else:
				sys.exit()
				
			countItNextTime = False
		#elif data[n] == 'x' and n>0 and data[n-1] == '0' and (n<len(data)-3) and self.charIsValidHex(data[n+1]) and self.charIsValidHex(data[n+2]):
		elif data[n] == 'x' and n>0 and data[n-1] == '0' and (n<len(data)-3) and charIsValidHex(data[n+1]) and charIsValidHex(data[n+2]):
			hex0xPrefixCount += 1
		else:
			hexCharArray = []
			binaryArray = ""
			
			PRINT ("\n"*3,"REAL Binary file, NOT Textified hex","\n"*3,)
			return False
			nonHexCharCount += 1

	PRINT ( "hexCharCount =", hexCharCount)
	PRINT ( "spaceCount =", spaceCount)
	PRINT ( "hex0xPrefixCount =", hex0xPrefixCount)
	PRINT ( "nonHexCharCount =", nonHexCharCount)
	PRINT ( len(hexCharArray),"-size hexCharArray =", hexCharArray)
	PRINT ( len(binaryArray),"-size binaryArray =", binaryArray)
	
	return True


##############################################################################################
# This function populates the unraveled list
##############################################################################################
def populateUnraveled():
	global unraveled
	
	del unraveled[:]
	
	for N in range(len(variablesAtGlobalScopeSelected)):
		itemFound = False
		for item in sizeOffsets:	# We do not know which order the sizeOffsets is sorted, hence need to find it
			if item[0] == variablesAtGlobalScopeSelected[N]:
				variableId = 		item[0]
				currentOffset =     item[1]
				currentlength =     item[2]
				selectedVariable = variableDeclarations[variableId]
				itemFound = True
				break;
		if not itemFound:
			OUTPUT("ERROR - did not find variablesAtGlobalScopeSelected[",N,"] =",variablesAtGlobalScopeSelected[N])
			sys.exit()
		PRINT (N,". Inside mapStructureToData(), Processing selectedVariable =",selectedVariable )
#			PRINT ("unraveled = ",unraveled)
		printUnraveled()
		variableName 					= selectedVariable[0]
		variableSize 					= selectedVariable[1]
		variableDescription 			= selectedVariable[4]
		baseType						= variableDescription["baseType"]	# For a declaration like int * pInt; baseType is int, but datatype is pointer
		datatype						= variableDescription["datatype"]   # That's the difference between baseType and datatype
		PRINT ("baseType = ",baseType)
		PRINT ("datatype = ",datatype)
		
		level = 0
		if variableDescription["isArray"]:
			arrayElementSize = variableDescription["arrayElementSize"]
			arrayDimensions = variableDescription["arrayDimensions"]
			totalNumberOfArrayElements = listItemsProduct(arrayDimensions)
			dimensionsText = STR(arrayDimensions[0])
			for d in range(1,len(arrayDimensions)):
				dimensionsText += " X "+ STR(arrayDimensions[d])
			dataTypeText = "unsigned" + " " + datatype if datatype != "pointer" and variableDescription["signedOrUnsigned"] == "unsigned" else datatype
			arrayDescriptionText = variableName + " - Array of "+ dimensionsText + " " + dataTypeText + "s"
			
			unraveled.append([level,arrayDescriptionText,variableDescription, currentOffset, currentOffset+arrayElementSize*totalNumberOfArrayElements])
			
			for position in range(totalNumberOfArrayElements):
				arrayIndices = calculateArrayIndicesFromPosition(arrayDimensions, position)
				arrayIndicesCStyle = ""	# We convert the [i,j,k] to C-style [i][j][k]
				for item in arrayIndices:
					arrayIndicesCStyle += "["+STR(item)+"]"
				arrayElementIndexDescription = STR(variableName) + arrayIndicesCStyle
				elementOffset = currentOffset + position * arrayElementSize
				if datatype in getDictKeyList(structuresAndUnionsDictionary):
					PRINT ("datatype = ",datatype, "is a struct")
					
					unravelNestedStructResult = unravelNestedStruct(level+1, datatype, arrayElementIndexDescription, elementOffset)
					
					if unravelNestedStructResult == False:
						warningMessage = "WARNING - false return result from unravelNestedStruct()!" 
						warningRoutine(warningMessage)
				else:
					PRINT ("datatype = ",datatype, "is NOT a struct")
					
					unraveled.append([level+1,arrayElementIndexDescription,variableDescription, elementOffset, elementOffset+arrayElementSize])
					
		elif datatype in getDictKeyList(structuresAndUnionsDictionary):
			PRINT ("datatype = ",datatype, "is a struct")
			
			unravelNestedStructResult = unravelNestedStruct(level, datatype, variableName, currentOffset)
			
			if unravelNestedStructResult == False:
				warningMessage = "WARNING - false return result from unravelNestedStruct()!" 
				warningRoutine(warningMessage)
		else:
			PRINT ("datatype = ",datatype, "is NOT a struct")
			
			unraveled.append([level,variableName, variableDescription, currentOffset, currentOffset+currentlength])
			

	PRINT ("\n\nBefore adding value to unraveled, unraveled =")
	PRINT ("\n","=="*100,"\n\n" )
		
	printUnraveled();
	
	# Now that unraveled list has been populated, lets fill out their values. First read the block
	
	if len(dataBlock) == 0:
		OUTPUT("\n\nWARNING - dataBlock is empty - Nothing to show")
#		sys.exit()
		return
	else:
		PRINT("Before populating unraveled with data from dataBlock, len(dataBlock) = ",len(dataBlock))

		PRINT ("Before adding value to unraveled, extended unraveled =")
		for N in range(len(unraveled)):
			PRINT ("unraveled[",N,"] =",unraveled[N])
			if N<len(unraveled)-1 and unraveled[N][0]==unraveled[N+1][0]-1:	# The current node is a parent
				unraveled[N].extend(["","",""])
			else:
				if isinstance(unraveled[N][2],dict) and unraveled[N][2]["datatype"].startswith("function "):
					unraveled[N].extend(["","",""])
				else:
					# Don't forget to deduct the dataLocationOffset, since the dataBlock is essentially a block with indices 0 through totalBytesToReadFromDataFile-1
					if unraveled[N][2]["isBitField"]:
						bitFieldWidth = unraveled[N][2]["bitFieldWidth"]
						datatype = unraveled[N][2]["bitFieldInfo"]["currentBitFieldSequenceContainerDatatype"]
						numBytesToRead = unraveled[N][2]["bitFieldInfo"]["currentBitFieldSequenceContainerSizeInBytes"]
						bitIndexStart = unraveled[N][2]["bitFieldInfo"]["currentBitFieldSequenceCurrentContainerBitIndexStart"]
						bitIndexEndInclusive = unraveled[N][2]["bitFieldInfo"]["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"]
						if bitFieldWidth != bitIndexEndInclusive - bitIndexStart + 1:
							PRINT ("Mismatching bitwidth for N = ",N)
							sys.exit()
					else:
						bitFieldWidth = 0
						bitIndexStart = 0
						datatype = unraveled[N][2]["datatype"]
						numBytesToRead = primitiveDatatypeLength[datatype]

					# Full data is there
#					if unraveled[N][3]-dataLocationOffset+numBytesToRead < len(dataBlock):		# Left to show bug - if there is a single item, this check will fail
					if unraveled[N][3]-dataLocationOffset+numBytesToRead <= len(dataBlock):		
						valueBytes = dataBlock[unraveled[N][3]-dataLocationOffset : unraveled[N][3]-dataLocationOffset+numBytesToRead]
						signedOrUnsigned = unraveled[N][2]["signedOrUnsigned"]
						PRINT ("Calling internalValueLittleEndian()/internalValueBigEndian() for variable ",unraveled[N][0],"datatype =",datatype, "bitFieldWidth =",bitFieldWidth,"bitIndexStart =",bitIndexStart)
						valueLE = calculateInternalValue(valueBytes, LITTLE_ENDIAN, datatype, signedOrUnsigned,bitFieldWidth,bitIndexStart)
						valueBE = calculateInternalValue(valueBytes, BIG_ENDIAN, datatype, signedOrUnsigned,bitFieldWidth,bitIndexStart)
						unraveled[N].extend([printHexStringWord(valueBytes),valueLE,valueBE])
					# Partial data is there
					elif unraveled[N][3]-dataLocationOffset < len(dataBlock):
						valueBytes = dataBlock[unraveled[N][3]-dataLocationOffset : unraveled[N][3]-dataLocationOffset+numBytesToRead]
						unraveled[N].extend([printHexStringWord(valueBytes),"Incomplete","Incomplete"])
					else:
						unraveled[N].extend(["No data","Unknown","Unknown"])

		PRINT ("\n\nAfter adding value to unraveled, unraveled =")
		printUnraveled()


##############################################################################################
# This function does a pretty printing of the unraveled list
##############################################################################################
def prettyPrintUnraveled():
	PRINT("\n\n\n","==="*50,"\nInside prettyPrintUnraveled()\n","==="*50)
	if unraveled == []:
		return True
	
	OUTPUT ("\n\n\n\n")
	OUTPUT ("=="*80)
	OUTPUT ("M A P P I N G    O F    T H E   L A Y O U T     O N T O    T H E     D A T A")
	OUTPUT ("=="*80)
	OUTPUT ("\n\n")
	
	unraveledColumnMaxWidths = []
	
	treeViewAllRowsValues = []
	
	maxNumberOfColumns = len(treeViewHeadings)
	for N in range(len(unraveled)):
		# The first column is the level #, which we do not display
		maxNumberOfColumns = len(unraveled[N])-1 if len(unraveled[N])-1 > maxNumberOfColumns else maxNumberOfColumns
	
	if maxNumberOfColumns > len(treeViewHeadings):
		PRINT ("ERROR: There are more fields (",maxNumberOfColumns,") in unraveled than number of headings (",len(treeViewHeadings),")")
		for N in range(len(unraveled)):
			if len(unraveled[N])== maxNumberOfColumns:
				PRINT ("unraveled[",N,"] = ",unraveled[N])
		sys.exit()
		
	#PRINT ("maxNumberOfColumns =",maxNumberOfColumns)
	
	for c in range(maxNumberOfColumns):
		unraveledColumnMaxWidths.append(len(treeViewHeadings[c]))

	for N in range(len(unraveled)):
		PRINT("Hi")
		PRINT ("\nN =",N, "unraveled[",N,"][2] =",unraveled[N][2],"\n\n")
		PRINT ("BYE")
		levelIndent = "    " * unraveled[N][0]
		dataTypeText = unraveled[N][2] if not isinstance(unraveled[N][2],dict) else unraveled[N][2]["datatype"] if unraveled[N][2]["signedOrUnsigned"] != "unsigned" or unraveled[N][2]["datatype"] == "pointer" else unraveled[N][2]["signedOrUnsigned"] + " " + unraveled[N][2]["datatype"]
		if N<len(unraveled)-1 and unraveled[N][0]==unraveled[N+1][0]-1 and isinstance(unraveled[N][2],dict) and unraveled[N][2]["isArray"]:	# The current node is a parent - an array 
			dataTypeText += " array"
		if isinstance(unraveled[N][2],dict) and unraveled[N][2]["datatype"].startswith("function "):	# Hardcode it for functions
			dataTypeText = "function"
		if isinstance(unraveled[N][2],dict) and ("isBitField" in getDictKeyList(unraveled[N][2])) and unraveled[N][2]["isBitField"]:
			isBitField = unraveled[N][2]["isBitField"]
			bitFieldInfo = unraveled[N][2]["bitFieldInfo"]
		else:
			isBitField = False
			
		try:
			if isBitField:
				addrStart = hex(unraveled[N][3]+integerDivision(bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"],BITS_IN_BYTE)) + "." + STR(bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"]%BITS_IN_BYTE)
				addrEnd = hex(unraveled[N][3]+integerDivision(bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"],BITS_IN_BYTE)) + "." + STR(bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"]%BITS_IN_BYTE)
			else:
				addrStart = hex(unraveled[N][3])
				addrEnd = hex(unraveled[N][4]-1)
			
			treeViewSingleRowValues = [levelIndent+unraveled[N][1], dataTypeText,addrStart,addrEnd,unraveled[N][5],STR(unraveled[N][6]),STR(unraveled[N][7])]
			treeViewAllRowsValues.append(treeViewSingleRowValues)
		except IndexError:
			OUTPUT ("IndexError in prettyPrintUnraveled(): List index out of range for N = ",N)
			OUTPUT ("unraveled[N] =", unraveled[N])
			OUTPUT ("treeViewAllRowsValues = ")
			OUTPUT (treeViewAllRowsValues)
			sys.exit()
		for c in range(len(treeViewSingleRowValues)):
			newLength = 0 if treeViewSingleRowValues[c] == None else 5 if type(treeViewSingleRowValues[c]) == bool else len(treeViewSingleRowValues[c])
			unraveledColumnMaxWidths[c] = newLength if newLength > unraveledColumnMaxWidths[c] else unraveledColumnMaxWidths[c]

	# Now that we have gotten the maximum length, let's print it
	headerString = ""
	bottomLine = ""
	for c in range(maxNumberOfColumns):
		# The last 3 column headers need to be right-justified
		if c < maxNumberOfColumns-5:
			headerString +=         treeViewHeadings[c] +" "* (unraveledColumnMaxWidths[c]-len(treeViewHeadings[c])) + "   "
			bottomLine   += "="*len(treeViewHeadings[c])+" "* (unraveledColumnMaxWidths[c]-len(treeViewHeadings[c])) + "   "
		else:
			headerString += " "* (unraveledColumnMaxWidths[c]-len(treeViewHeadings[c])) +         treeViewHeadings[c] + "   "
			bottomLine   += " "* (unraveledColumnMaxWidths[c]-len(treeViewHeadings[c])) + "="*len(treeViewHeadings[c])+ "   "
	OUTPUT (bottomLine)
	OUTPUT (headerString)
	OUTPUT (bottomLine)
		
	for N in range(len(treeViewAllRowsValues)):
		rowText = ""
		for c in range(len(treeViewAllRowsValues[N])):
			lengthCurrentItem = len(treeViewAllRowsValues[N][c]) if not checkIfBoolean(treeViewAllRowsValues[N][c]) else 5 
			currentItem = treeViewAllRowsValues[N][c] if not checkIfBoolean(treeViewAllRowsValues[N][c]) else "True " if treeViewAllRowsValues[N][c] else "False"
			if c <= 1:
				rowText += currentItem + " "* (unraveledColumnMaxWidths[c]-lengthCurrentItem) + "   "
			else:
				rowText += " "* (unraveledColumnMaxWidths[c]-lengthCurrentItem) + currentItem + "   "
		OUTPUT (rowText)

	
	# Write the header and data to a snapshot file
	while True:
		try:
			outputFile = open(SNAPSHOT_FILE_NAME,"w")
			break
		except IOError:
			warningMessage = "WARNING: cannot open the "+SNAPSHOT_FILE_NAME+" file for writing - possibly already open. Please close it and only then press OK here."
			warningRoutine(warningMessage)
			return False
	headerString = ""
	for c in range(maxNumberOfColumns):
		headerString += treeViewHeadings[c] + ("," if c < maxNumberOfColumns-1 else "\n")
	outputFile.write(headerString)
			
	for N in range(len(treeViewAllRowsValues)):
		rowText = ""
		for c in range(maxNumberOfColumns):
			currentItem = treeViewAllRowsValues[N][c] if not checkIfBoolean(treeViewAllRowsValues[N][c]) else "True " if treeViewAllRowsValues[N][c] else "False"
			rowText += currentItem + ("," if c < maxNumberOfColumns-1 else "\n")
		outputFile.write(rowText)
		
	outputFile.close()
	return True

def dumpDetailsForDebug(MUST=False):
	global PRINT_DEBUG_MSG
	
	PRINT_DEBUG_MSG_backed_up = PRINT_DEBUG_MSG
	
	if MUST:
		PRINT_DEBUG_MSG = True
	
	PRINT ("\n"*3,"=="*50,"\nBEGIN Dumping data for debug\n","=="*50,"\n"*3)

	PRINT ("pragmaPackStack =",pragmaPackStack)
	PRINT ("dataLocationOffset = ",dataLocationOffset )
	PRINT ("fileDisplayOffset =",fileDisplayOffset )
	PRINT ("totalBytesToReadFromDataFile =",totalBytesToReadFromDataFile)
	PRINT ("len(dataBlock) =",len(dataBlock))
	PRINT ("size of variableDeclarations =",len(variableDeclarations) )
	PRINT ("\n"*3,"==="*50,"\nstructuresAndUnionsDictionary\n","=="*50 )
	for item in structuresAndUnionsDictionary:
		PRINT ("\n",item, ":", structuresAndUnionsDictionary[item])
	PRINT ("=="*50,"\n"*3 )
	PRINT ("\n"*3,"==="*50,"\nvariableDeclarations\n","=="*50 )
	for item in variableDeclarations:
		PRINT ("\n",item )
	PRINT ("=="*50,"\n"*3 )
	PRINT ("\nglobalScopes[variableId, scopeStartVariableId, scopeEndVariableId]) =\n")
	for item in globalScopes:
		PRINT (item, variableDeclarations[item[0]][0])
	PRINT ("\nglobalScopesSelected [variableId, scopeStartVariableId, scopeEndVariableId]) =\n")
	if globalScopesSelected:
		for item in globalScopesSelected:
			PRINT (item)
			PRINT (variableDeclarations[item[0]][0])
	PRINT ("variablesAtGlobalScopeSelected =",variablesAtGlobalScopeSelected)
	PRINT ("variablesAtGlobalScopeSelected =",[variableDeclarations[item][0] for item in variablesAtGlobalScopeSelected])
	PRINT ("variableSelectedIndices =",variableSelectedIndices)
	PRINT ("variableSelectedIndices =",[variableDeclarations[item][0] for item in variableSelectedIndices])
	PRINT ("\n"*3,"==="*50,"\nsizeOffsets <start (inclusive), end (not inclusive)> \n","=="*50 )
	for item in sizeOffsets:
		PRINT("<",item[1],"(",HEX(item[1]),"),",item[1]+item[2],"(",HEX(item[1]+item[2]),")> (length", item[2],") for",variableDeclarations[item[0]][0],)
	PRINT ("\n"*3,"=="*50,"\nunraveled\n","=="*50 )
	printUnraveled()
	PRINT ("\n"*3,"=="*50,"\n END Dumping data for debug\n","=="*50,"\n"*3)

	if MUST:
		PRINT_DEBUG_MSG = PRINT_DEBUG_MSG_backed_up


def openDataFileRoutineBatch(dataFileNameInput):
	global dataFileName, dataFileSizeInBytes, inputIsHexChar
	
	if dataFileNameInput and os.path.exists(dataFileNameInput):
	
		dataFileName = dataFileNameInput
	
		inputIsHexChar = False
		# Check if it is binary file, or text version of a hex file
		if inputFileIsHexText():
			inputIsHexChar = True
			PRINT ("WARNING: Input file is Hex text")
			
			dataFileSizeInBytes = len(binaryArray)
		else:
			dataFileSizeInBytes = os.path.getsize(dataFileName)
		return True
	else:
		OUTPUT ("dataFileName = ",dataFileNameInput,"is not valid - exiting!")
		return False

# The other routine, updateDisplayBlock(), reads a fixed-size displayBlock. This, OTOH, reads any-length block from anywhere, and returns that block.
# This is useful when the data to be retrived are outside the BLOCK_SIZE display window. Two cases that are specifically useful are:

def readBytesFromFile(startAddress, numBytesToRead):
	if len(binaryArray)>0:
		blockRead = binaryArray[startAddress: startAddress+numBytesToRead]
	else:
		with open(dataFileName, "rb") as file:
			try:
				file.seek(startAddress, os.SEEK_SET)
				blockRead = file.read(numBytesToRead)
			except ValueError: 
				PRINT ("ValueError on trying to read ",numBytesToRead,"bytes from file offset",startAddress )
				return False
			except:
				PRINT ("Unknown error while trying to read the file - exiting")
				sys.exit()
	PRINT ("type(blockRead) = ",type(blockRead))	# str in Python 2, but bytes in Python 3
	PRINT ("len(blockRead) = ",len(blockRead))
	if len(blockRead) != numBytesToRead:
		warningrMessage = "ERROR in readBytesFromFile(): From Offset " + STR(startAddress) + " wanted to read "+ STR(numBytesToRead)+" bytes, but succeeded reading only "+STR(len(blockRead))+" bytes instead!"
		warningRoutine(warningrMessage)
		dumpDetailsForDebug()
		#return False
		#sys.exit()
	return blockRead

############################################################################################################################
############################################################################################################################
#
# interpret - Batch portion
#
############################################################################################################################
############################################################################################################################

def interpretBatch():
	global lines, tokenLocationLinesChars, enums, enumFieldValues, typedefs, structuresAndUnionsDictionary, unraveled
	global dummyVariableCount, totalVariableCount, globalScopes, sizeOffsets, variablesAtGlobalScopeSelected
	global pragmaPackCurrentValue, pragmaPackStack

	PRINT ("\n\n\n============ Entered interpretBatch() ==================\n\n\n")

	pragmaPackCurrentValue = None
	pragmaPackStack = []
	tokenLocationLinesChars = []
	variableDeclarations = []
	unraveled = []
	enums.clear()
	enumFieldValues.clear()
	typedefs.clear()
	structuresAndUnionsDictionary.clear()
	dummyVariableCount = 0
	totalVariableCount = 0
	globalScopes = []
	sizeOffsets = []
	variablesAtGlobalScopeSelected = []
	dataBlock = []

	# Call the main module
	mainWorkOutput = mainWork()
	if mainWorkOutput == False:
		OUTPUT ("ERROR in interpretBatch() after calling mainWork() - exiting" )
		return False

def calculateSizeOffsetsBatch():
	global sizeOffsets, totalBytesToReadFromDataFile
	
	sizeOffsets = []
	
	if not variablesAtGlobalScopeSelected:
		PRINT("No variable at Global scope selected")
		#if sizeOffsets:
		#	OUTPUT("Something fishy: variablesAtGlobalScopeSelected is empty but sizeOffsets is not - exiting")
		#	sys.exit()
		return
		
	beginOffset = dataLocationOffset
	for variableId in variablesAtGlobalScopeSelected:
		sizeOffsets = getOffsetsRecursively(variableId, sizeOffsets, beginOffset)
		beginOffset += variableDeclarations[variableId][1]
	totalBytesToReadFromDataFile = beginOffset - dataLocationOffset
	
	PRINT("\n\n\nBefore sorting sizeOffsets\n\n")
	PRINT("sizeOffsets =",sizeOffsets)
	for item in sizeOffsets:	
		PRINT(variableDeclarations[item[0]][0],"<",item[1],",",item[1]+item[2],"> (length", item[2],") <start (inclusive), end (not inclusive)>")
	sizeOffsets.sort(key=lambda list3rdItem: list3rdItem[2], reverse=True)
	PRINT("\n\n\ntotalBytesToReadFromDataFile =",totalBytesToReadFromDataFile,"\n\n")
	PRINT("\n\n\nAfter sorting sizeOffsets\n\n")
	for item in sizeOffsets:	
		PRINT(variableDeclarations[item[0]][0],"<",item[1],",",item[1]+item[2],"> (length", item[2],") <start (inclusive), end (not inclusive)>")
	#PRINT("variableDeclarations =",variableDeclarations)
	dumpDetailsForDebug()

	hasBitfields = False
	for item in sizeOffsets:
		if variableDeclarations[item[0]][4]['isBitField']== True:
			hasBitfields = True
	
	# Sanity check. Remember that this straight-up addition would not work for bitfield, since there many different variables would occupy the same container.
	min = 10000000000000000000000
	max = -1
	for item in sizeOffsets:
		if item[1]<min:
			min = item[1]
		if item[1]+item[2] > max:
			max = item[1]+item[2]
	if min != dataLocationOffset:
		OUTPUT("min (",min,") != dataLocationOffset (",dataLocationOffset,") - exiting")
		sys.exit()
	if max != dataLocationOffset+totalBytesToReadFromDataFile and hasBitfields == False:
		OUTPUT("max (",max,") != dataLocationOffset (",dataLocationOffset,") + totalBytesToReadFromDataFile (",totalBytesToReadFromDataFile,")")
		sys.exit()

############################################################################################
#  
#  process in the Batch mode
#
############################################################################################

def processBatch():
	global lines, variablesAtGlobalScopeSelected, dataBlock, PRINT_DEBUG_MSG

	PRINT("Inside processBatch()")
	
	if not BATCHMODE:
		OUTPUT ("ERROR - being asked to process in batchmode when BATCHMODE is False")
		sys.exit()
	
	if codeFileName and os.path.exists(codeFileName):
		with open(codeFileName, "r") as codeFile:
			try:
				lines = codeFile.readlines()
				if not checkIfStringOrListOfStrings(lines):
					errorMessage = "ERROR in coding: input code file content is NOT string - type(lines) = "+STR(type(asciiLines))
					errorRoutine(errorMessage)
					return False
				
			except ValueError: # Empty file
				return False
	else:
		OUTPUT("ERROR - cannot open code file",codeFileName)
		sys.exit()
		
	PRINT ("Code file contains:", lines )

	PRINT ("calling interpretBatch()")
	interpretBatchResult = interpretBatch()

	# Call the main module
	if interpretBatchResult == False:
		OUTPUT ("ERROR in interpret() after calling mainWork() - exiting" )
		return False
	else:
		PRINT("Successfully executed interpretBatchResult()")

	# Instead of mapping, we create straightaway say everything at global scope is selected (unless it is a typedef and we are not mapping that)
	variablesAtGlobalScopeSelected = []
	for i in range(len(globalScopes)):
		varIndex = globalScopes[i][0]
		PRINT("i =",i,"variableDeclarations[varIndex] =",variableDeclarations[varIndex])
		if 'typedef' in variableDeclarations[varIndex][2]: 
			if MAP_TYPEDEFS_TOO:
				PRINT("Counting typedefs")
				# There is a special case - where we are using builtin typedefs, and we are mapping typedefs too, but since it is builtin, there is no code to actual color
				if variableDeclarations[varIndex][4]["globalTokenListIndex"] >= 0:
					variablesAtGlobalScopeSelected.append(varIndex)
			else:	
				PRINT("Cannot count typedefs")
			pass
		else:
			PRINT("Counting non-typedef")
			variablesAtGlobalScopeSelected.append(varIndex)
	
	if inputVariables:
		allPossibleGlobalVariableNames = [variableDeclarations[variableId][0] for variableId in variablesAtGlobalScopeSelected]
		globalsToKeep = []
		PRINT("allPossibleGlobalVariableNames =",allPossibleGlobalVariableNames)
		PRINT("Keeping only the list of the user-supplied variables (assuming they are indeed global): ",inputVariables)
		for variableId in variablesAtGlobalScopeSelected:
			variableName = variableDeclarations[variableId][0]
			if variableName in inputVariables:
				globalsToKeep.append(variableId)
		PRINT("After processing the input list, globalsToKeep =",[variableDeclarations[variableId][0] for variableId in globalsToKeep])
		if globalsToKeep:
			variablesAtGlobalScopeSelected = globalsToKeep
		else:
			OUTPUT("None of the user-supplied variables are in the global list - hence displaying ALL global variables")
	
	PRINT("Now going to execute calculateSizeOffsetsBatch()")
	calculateSizeOffsetsBatch()
	PRINT("Now going to read", totalBytesToReadFromDataFile, "bytes from the data file")

	# Now read the data file - possibly delete
	if not openDataFileRoutineBatch(dataFileName):
		OUTPUT("Error opening data file",dataFileName)
		sys.exit()
	
	if dataFileSizeInBytes < totalBytesToReadFromDataFile:
		PRINT("WARNING: Input file smaller than provided file format/structure - not all values would be displayable")
	dataBlock = readBytesFromFile(dataLocationOffset, totalBytesToReadFromDataFile)
	if len(dataBlock) != min(totalBytesToReadFromDataFile,dataFileSizeInBytes-dataLocationOffset):
		OUTPUT("ERROR in reading data file, was able to read only",len(dataBlock),"bytes of data while trying to read",totalBytesToReadFromDataFile,"bytes from",dataFileSizeInBytes,"-byte-sized data file")
		sys.exit()
#	PRINT_DEBUG_MSG = True
#	dumpDetailsForDebug()
#	PRINT_DEBUG_MSG = False

	PRINT("Now going to populate the unraveled")

	# Populate the unraveled
	populateUnraveled()
	PRINT("Now going to print the unraveled")
	prettyPrintUnraveled()
	PRINT("THE END")
		
def main():
	
	global window, BATCHMODE, MAINLOOP_STARTED

	if not BATCHMODE:
		try:
			app = tk.Tk()
		except tk.TclError:
			OUTPUT("Error in instantiating GUI - resorting to batch mode")
			BATCHMODE = True
	
	parseCommandLineArguments()

	if BATCHMODE:
		processBatch()
	elif not BATCHMODE:
		try:
			app.title(TOOL_NAME)
			window = MainWindow(app)
			app.protocol("WM_DELETE_WINDOW", window.quit)
			app.resizable(width=False, height=False)
			
			if IN_DEMO:
				window.runDemo()
				
			MAINLOOP_STARTED = True
			app.mainloop()
		except tk.TclError:
			OUTPUT("Error in instantiating GUI - exiting!")
			sys.exit()
	else:
		OUTPUT("Unknown value of BATCHMODE =",BATCHMODE)
		sys.exit()

class MainWindow:

	def __init__(self, parent):
		self.parent = parent
		self.validateCommandDataOffsetEntry = parent.register(self.validateRoutineDataOffsetEntry)		# Data location offset
		self.validateCommandFileOffsetEntry = parent.register(self.validateRoutineFileOffsetEntry)		# File display  offset
		self.createGUIvariables()
		self.createWidgets()
		self.createToolLayout()
		self.create_bindings()
		
		if codeFileName:
			self.openCodeFile(codeFileName)
		if dataFileName:
			self.openDataFile(dataFileName)

		# Explicitly set
		if dataLocationOffset != 0:
			self.dataOffsetEntry.insert(tk.END,dataLocationOffset)
		
	def createGUIvariables(self):
#		self.dataFileSizeInBytes = None
#		self.tokenLocationLinesChars = []
#		self.dataFileName = None

		# This variable has a special purpose. We have trace variables associated with the self.fileOffset, which means every time it changes, the data window gets re-displayed.
		# We also have a special handling of self.fileOffset variable - if it is blank, set it to 0.
		# Unfortunately, this creates a particular problem - we can never update it properly. That's because, on the IntVar variable in Tcl/Tk, there is no "direct" update method -
		# you have to first delete it and only then insert it. However, the moment you delete it, it gets blanked out, and gets reset to 0. And due to trace, we re-display.
		# So, now when you re-insert your intended value, it's going to have an extra 0 at the end, thereby effectively multiplying it by 10.
		# So, we want to solve two problems. We want to stop re-displaying the data windows until they are really ready.
		self.OK2reDisplayDataWindows = False 	# We will set it to True at the end of this routine
		
		# This is modified by both SpinBox (directly) and the Entry to its right (indirectly)
		self.fileOffset = tk.IntVar()
		PRINT("Inside createGUIvariables(), doing self.fileOffset.set(0)")
		self.fileOffset.set(0)
		PRINT("Inside createGUIvariables(), did self.fileOffset.set(0)")
		
		# There are two variables associated with the data offset.
		# 1. The one where you can enter any text (like 1MB/2+0x13). This is NOT an int-only field, hence we need a StringVar.
		# 2. The integer variable (self.dataOffset) that we deduce from the above string.
		
		self.dataOffset = tk.IntVar()		
		PRINT("Inside createGUIvariables(), doing self.dataOffset.set(0)")
		self.dataOffset.set(0)
		PRINT("Inside createGUIvariables(), did self.dataOffset.set(0)")
		
		
		self.dataOffsetEntryVariable = tk.StringVar()
		self.fileOffsetEntryVariable = tk.StringVar()
		
		self.originalCodeTextVariable = tk.StringVar()		# We do not need another similar variable for the Interpreted code window since that is supposed to be used as Rread-only
		
		self.colorTagsData = []
		self.colorTagsCode = []
		self.COLORS = []
		self.currentCoordinates = ""

		self.OK2reDisplayDataWindows = True
		
		# This array/list is created for a very special reason. Suppose after coloring code and data, we take our cursor over certain data items, 
		# and as a result the corresponding variable in the Interpreted Code gets background-highlighted.
		# Now, imgine doing a Page down. You did not really move the cursor, do the <Leave> routine will not get triggered. 
		# As a result, the highlighting in the Interpreted Code window will remain.
		# This is NOT just a problem with Page Up or Page Down
		self.interpretedCodeVariablesHighlightedStartEndCoordinates = []

	def validateRoutineDataOffsetEntry(self, P):
		PRINT ("Inside validateRoutineDataOffsetEntry() Passed parameter(P) =",P,"type(P) =",type(P))
		self.dataOffsetEntryVariable.set(P)
		humanReadableOffsetString = self.dataOffsetEntryVariable.get()
		PRINT ("Currently self.dataOffsetEntryVariable =",humanReadableOffsetString)
		if humanReadableOffsetString.strip() == "":
			self.dataOffset.set(0)
			self.dataOffsetEntry.delete(0, tk.END)
			# If we are returning False, the dataOffsetEntry will get disabled. So here is a hack to enable it from outside
#			self.frame.after_idle(lambda: self.dataOffsetEntry.config(validate='focusout'))	
			self.frame.after(1000,lambda: self.dataOffsetEntry.config(validate='focusout'))	 
			return False
		else:
			result = convertByteUnits2Decimal(humanReadableOffsetString)
			if result[0] == False:
				self.frame.after(1000,lambda: self.dataOffsetEntry.config(validate='focusout'))	
				return False
			else:
				offsetValue = result[1]
			PRINT ("Data location offset of <",humanReadableOffsetString,"> resolves to ",offsetValue)
			if offsetValue < 0:
				errorMessage = STR(humanReadableOffsetString)+ " resolves to "+STR(offsetValue)+", which is not a valid data offset"
				errorRoutine(errorMessage)
				self.frame.after(1000,lambda: self.dataOffsetEntry.config(validate='focusout'))	
				return False
			elif offsetValue >= dataFileSizeInBytes:
				errorMessage = STR(humanReadableOffsetString)+ " resolves to "+STR(offsetValue)+", which is not a valid data offset as file size iteself is "+STR(dataFileSizeInBytes)
				errorRoutine(errorMessage)
				self.frame.after(1000,lambda: self.dataOffsetEntry.config(validate='focusout'))	
				return False
			else:
				PRINT("\n"*3,"=="*50,"\n Now going to re-display data for data location offset %d\n"%offsetValue,"=="*50,"\n"*2)
				self.dataOffset.set(offsetValue)
				self.showDataBlock()
				return True

	def validateRoutineFileOffsetEntry(self, P):	
		PRINT( "Inside validateRoutineFileOffsetEntry() Passed parameter(P) =",P,"type(P) =",type(P))
		self.fileOffsetEntryVariable.set(P)
		humanReadableOffsetString = self.fileOffsetEntryVariable.get()
		PRINT ("Currently self.fileOffsetEntryVariable =",humanReadableOffsetString)
		if humanReadableOffsetString.strip() == "":
			self.fileOffsetEntry.delete(0, tk.END)
			# If we are returning False, the fileOffsetEntry will get disabled. So here is a hack to enable it from outside
#			self.frame.after_idle(lambda: self.fileOffsetEntry.config(validate='focusout'))	
			self.frame.after(1000,lambda: self.fileOffsetEntry.config(validate='focusout'))	
			return False
		else:
			result = convertByteUnits2Decimal(humanReadableOffsetString)
			if result[0] == False:
				self.frame.after(1000,lambda: self.fileOffsetEntry.config(validate='focusout'))	
				return False
			else:
				offsetValue = result[1]
			PRINT (humanReadableOffsetString," resolves to ",offsetValue)
			if offsetValue < 0:
				errorMessage = STR(humanReadableOffsetString)+ " resolves to "+STR(offsetValue)+", which is not a valid file offset"
				errorRoutine(errorMessage)
				self.frame.after(1000,lambda: self.fileOffsetEntry.config(validate='focusout'))	
				return False
			elif offsetValue >= dataFileSizeInBytes:
				errorMessage = STR(humanReadableOffsetString)+ " resolves to "+STR(offsetValue)+", which is not a valid file offset as file size iteself is "+STR(dataFileSizeInBytes)
				errorRoutine(errorMessage)
				self.frame.after(1000,lambda: self.fileOffsetEntry.config(validate='focusout'))	
				return False
			else:
				PRINT("\n"*3,"=="*50,"\n Now going to re-display data for file offset %d\n"%offsetValue,"=="*50,"\n"*2)
#				self.fileOffsetSpinbox.config(from_=offsetValue)
				PRINT ("Going to delete the self.fileOffsetSpinbox value")
				PRINT("Currently, self.fileOffsetSpinbox.get() =",self.fileOffsetSpinbox.get(),"self.fileOffset.get() =",self.fileOffset.get())
				self.OK2reDisplayDataWindows = False
				self.fileOffsetSpinbox.delete(0,"end")
				PRINT ("Deleted the self.fileOffsetSpinbox value.")
				self.OK2reDisplayDataWindows = True
				self.fileOffsetSpinbox.insert(0,offsetValue)
				PRINT ("After inserting the value of", offsetValue,"into the self.fileOffsetSpinbox, self.fileOffsetSpinbox.get() =",self.fileOffsetSpinbox.get(),"self.fileOffset.get() =",self.fileOffset.get())
				self.fileOffset.set(offsetValue)
				PRINT ("After performing self.fileOffset.set(offsetValue) where offsetValue =", offsetValue,"self.fileOffsetSpinbox.get() =",self.fileOffsetSpinbox.get(),"self.fileOffset.get() =",self.fileOffset.get())
				self.showDataBlock()
				return True
	
	def toggleDebug(self):
		global PRINT_DEBUG_MSG
		if PRINT_DEBUG_MSG:
			PRINT ("\nTurning Debug OFF\n")
			dumpDetailsForDebug()
			PRINT_DEBUG_MSG = False
			self.toggleDebugButton.config(text="Debug OFF")
		else:
			PRINT_DEBUG_MSG = True
			PRINT ("\nTurning Debug ON\n")
			self.toggleDebugButton.config(text="Debug ON")

	def toggleHexDec(self):
		global DISPLAY_INTEGRAL_VALUES_IN_HEX
		
		if DISPLAY_INTEGRAL_VALUES_IN_HEX == True:
			PRINT("Switching to Dec")
			DISPLAY_INTEGRAL_VALUES_IN_HEX = False
			self.toggleHexDecButton.config(text="Dec/Hex")
		else:
			PRINT("Switching to Hex")
			DISPLAY_INTEGRAL_VALUES_IN_HEX = True
			self.toggleHexDecButton.config(text="Hex/Dec")
		
		if lines:
			self.dataOffsetChange()
		

	def toggleRunOrClearDemo(self):
		global IN_DEMO
		
		if IN_DEMO == False:
			IN_DEMO = True
			self.toggleRunOrClearDemoButton.config(text="Clear Demo")
			self.runDemo()
		elif IN_DEMO == True:
			IN_DEMO = False
			self.toggleRunOrClearDemoButton.config(text="Run Demo")
			self.clearDemo()
		else:
			errorMessage = "ERROR in toggleRunOrClearDemo(), IN_DEMO value neither True nor False"
			errorRoutine(errorMessage)
		
	'''
	def toggleStructEndPadding(self):
		global COMPILER_PADDING_ON, STRUCT_END_PADDING_ON
		
		
		if STRUCT_END_PADDING_ON == True:
			if COMPILER_PADDING_ON == False:
				OUTPUT("ERROR - cannot have struct end-padding ON while compiler padding is OFF - existing")
				sys.exit()
			else:
				PRINT("Struct end-padding turned OFF")
				STRUCT_END_PADDING_ON = False
				self.toggleStructEndPaddingButton.config(text="Struct end-padding is OFF")
		elif STRUCT_END_PADDING_ON == False:
			PRINT("Compiler Padding turned ON")
			COMPILER_PADDING_ON = True
			self.toggleRunOrClearDemoButton.config(text="Compiler padding is ON")
			PRINT("Struct end-padding turned ON")
			STRUCT_END_PADDING_ON = True
			self.toggleStructEndPaddingButton.config(text="Struct end-padding is ON")
		else:
			sys.exit()
		
		if lines:
			self.interpret()
	'''

	def toggleMapTypedefsToo(self):
		global MAP_TYPEDEFS_TOO
		
		if MAP_TYPEDEFS_TOO == True:
			PRINT("Now typedefs would NO LONGER be treated as variable declarations (for data mapping purposes)")
			MAP_TYPEDEFS_TOO = False
			self.toggleMapTypedefsTooButton.config(text="Not mapping typedefs")
		elif MAP_TYPEDEFS_TOO == False:
			PRINT("Now typedefs would also be treated as variable declarations (for data mapping purposes)")
			MAP_TYPEDEFS_TOO = True
			self.toggleMapTypedefsTooButton.config(text="Mapping typedefs too")
		else:
			sys.exit()
		
		if lines:
			self.selectVariablesAtGlobalScope()
			self.dataOffsetChange()

				
	def createWidgets(self):
		frame = self.frame = ttk.Frame(self.parent)
		self.openCodeFileButton = ttk.Button(frame, text="Open code file", underline=5,command=self.openCodeFileDialogue)
		self.originalCodeLabel = ttk.Label(frame, text="Original code")
		self.interpretButton = ttk.Button(frame, text="Interpret", underline=0,command=self.interpret)
		self.interpretedCodeLabel = ttk.Label(frame, text="Interpreted code")
		self.mapButton = ttk.Button(frame, text="Map", underline=0,command=self.mapStructureToData)
		self.dataLocationOffsetLabel = ttk.Label(frame, text="Data starts at offset", underline=1)
		
		self.dataOffsetEntry = ttk.Entry(frame, text="dataOffsetEntry", validate="focusout", validatecommand=(self.validateCommandDataOffsetEntry, '%P'))
		if dataFileName == None:
			self.dataOffsetEntry.config(state=tk.DISABLED)
		
		self.openDataFileButton = ttk.Button(frame, text="Open data file", underline=0,command=self.openDataFileDialogue)
		self.fileOffsetLabel = ttk.Label(frame, text="from Offset", underline=0, width=12)
		self.fileOffsetSpinbox = Spinbox(frame, from_=0, textvariable=self.fileOffset, increment=BLOCK_SIZE)


		self.fileOffsetEntryLabel = ttk.Label(frame, text=" or ", width = 4)
		# Apparently, the text (or textvariable) has use - if we have two Entry widgets with the same text (or textvariable), they get "linked" by TCL
		# So, we MUST use different variables
		self.fileOffsetEntry = ttk.Entry(frame, text="fileOffsetEntry", validate="focusout", validatecommand=(self.validateCommandFileOffsetEntry, '%P'))
		if dataFileName == None:
			self.fileOffsetEntry.config(state=tk.DISABLED)
		
		toggleHexDecInitalText = "Hex/Dec" if DISPLAY_INTEGRAL_VALUES_IN_HEX else "Dec/Hex"
		self.toggleHexDecButton = ttk.Button(frame, text=toggleHexDecInitalText, underline=0,command=self.toggleHexDec)  
		toggleDebugInitalText = "Debug ON" if PRINT_DEBUG_MSG else "Debug OFF"
		self.toggleDebugButton = ttk.Button(frame, text=toggleDebugInitalText, underline=1,command=self.toggleDebug)  
		self.originalCodeText = tk.Text(self.frame, height=DISPLAY_BLOCK_HEIGHT, width=DISPLAY_BLOCK_WIDTH * 3)
		self.originalCodeTextVerticalScrollbar = ttk.Scrollbar(self.frame, command=self.originalCodeText.yview)
		self.interpretedCodeText = tk.Text(self.frame, height=DISPLAY_BLOCK_HEIGHT, width=DISPLAY_BLOCK_WIDTH * 3)
		self.interpretedCodeTextVerticalScrollbar = ttk.Scrollbar(self.frame, command=self.interpretedCodeText.yview)
		
		self.interpretedCodeText.config(state=tk.DISABLED)	# Initially, it should be disabled. Only Interpret should make it NORMAL

#		self.viewDataText = tk.Text(self.frame, height=DISPLAY_BLOCK_HEIGHT, width=4+(DISPLAY_BLOCK_WIDTH * 4))
		self.addressColumnText = tk.Text(self.frame, height=DISPLAY_BLOCK_HEIGHT, width=13)
		self.viewDataHexText = tk.Text(self.frame, height=DISPLAY_BLOCK_HEIGHT, width=(DISPLAY_BLOCK_WIDTH * 3))
		self.viewDataAsciiText = tk.Text(self.frame, height=DISPLAY_BLOCK_HEIGHT, width=(DISPLAY_BLOCK_WIDTH+1))
		self.CodeDataMeaningLabel = ttk.Label(frame, text="Description: ")
#		self.CodeDataMeaningText = ttk.Label(frame)										# MannaManna
		self.CodeDataMeaningText = ttk.Label(self.frame,wraplength=600,justify=tk.LEFT)
		self.dataAddressStartLabel = ttk.Label(frame, text="Address (start):")
		self.dataAddressEndLabel = ttk.Label(frame, text="Address (end):")
		self.dataAddressStartText = ttk.Label(frame)
		self.dataAddressEndText = ttk.Label(frame)
		self.dataLengthLabel = ttk.Label(frame, text="Length: ")
		self.dataLengthText = ttk.Label(frame)
		self.dataValueLELabel = ttk.Label(frame, text="Value (Little-Endian): ")
		self.dataValueBELabel = ttk.Label(frame, text="Value (Big-Endian)   : ")
		self.dataValueLEText = ttk.Label(frame)
		self.dataValueBEText = ttk.Label(frame)
#		self.treeView = ttk.Treeview(frame, height=8, displaycolumns='#all')		# Didn't work
		self.treeView = ttk.Treeview(frame, height=8)
		self.treeScroll = ttk.Scrollbar(frame, orient="vertical", command=self.treeView.yview)
		self.treeView.configure(yscrollcommand=self.treeScroll.set)
		toggleRunOrClearDemoInitalText = "Clear Demo" if IN_DEMO else "Run Demo"
		self.toggleRunOrClearDemoButton = ttk.Button(frame, text=toggleRunOrClearDemoInitalText, underline=9,command=self.toggleRunOrClearDemo)
		'''
		toggleStructEndPaddingInitalText = "Struct end-padding is ON" if STRUCT_END_PADDING_ON else "Struct end-padding is OFF"
		self.toggleStructEndPaddingButton = ttk.Button(frame, text=toggleStructEndPaddingInitalText, underline=0,command=self.toggleStructEndPadding)
		'''
		toggleMapTypedefsTooInitalText = "Mapping typedefs too" if MAP_TYPEDEFS_TOO else "Not mapping typedefs"
		self.toggleMapTypedefsTooButton = ttk.Button(frame, text=toggleMapTypedefsTooInitalText, underline=8,command=self.toggleMapTypedefsToo)
		
		self.createBasicTags()

	def createBasicTags(self):
		self.viewDataHexText.tag_configure("ascii", foreground="green")
		self.viewDataHexText.tag_configure("error", foreground="red")
		self.viewDataHexText.tag_configure("hexspace", foreground="navy")
		self.viewDataHexText.tag_configure("graybg", background="lightgray")
		self.viewDataHexText.tag_configure("yellowbg", background=HIGHLIGHT_COLOR)
		
		self.viewDataAsciiText.tag_configure("ascii", foreground="green")
		self.viewDataAsciiText.tag_configure("error", foreground="red")
		self.viewDataAsciiText.tag_configure("hexspace", foreground="navy")
		self.viewDataAsciiText.tag_configure("graybg", background="lightgray")
		self.viewDataAsciiText.tag_configure("yellowbg", background=HIGHLIGHT_COLOR)
		
		self.interpretedCodeText.tag_configure("yellowbg", background=HIGHLIGHT_COLOR)

	def createToolLayout(self):
		#####################
		# First Row widgets
		#####################
		
		# Widgets above the Original code window
		col = 0
		colSpan = 2
		self.openCodeFileButton.grid(row=0,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 2
		self.originalCodeLabel.grid(row=0,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 2
		self.interpretButton.grid(row=0,column=col, columnspan=colSpan, sticky=tk.W)
		
		# Widgets above the Interpreted code window
		col = col + colSpan
		colSpan = 2
		self.interpretedCodeLabel.grid(row=0,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.mapButton.grid(row=0,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.dataLocationOffsetLabel.grid(row=0, column=col, columnspan=colSpan, sticky=tk.E)
		col = col + colSpan
		colSpan = 2
		self.dataOffsetEntry.grid(row=0, column=col, columnspan=colSpan, sticky=tk.E)
		
		# Widgets above the Data display window
		col = 12
		colSpan = 1
		self.openDataFileButton.grid(row=0, column=col, columnspan=colSpan, sticky=tk.W) 
		col = col + colSpan
		colSpan = 1
		self.fileOffsetLabel.grid(row=0, column=col, columnspan=colSpan, sticky=tk.W) 
		col = col + colSpan
		colSpan = 1
		self.fileOffsetSpinbox.grid(row=0, column=col, columnspan=colSpan, sticky=tk.W) 
		col = col + colSpan
		colSpan = 1
		self.fileOffsetEntryLabel.grid(row=0, column=col, columnspan=colSpan, sticky=tk.W) 
		col = col + colSpan
		colSpan = 2
		self.fileOffsetEntry.grid(row=0, column=col, columnspan=colSpan, sticky=tk.W) 
		col = col + colSpan
		colSpan = 2
		self.toggleHexDecButton.grid(row=0, column=col, columnspan=colSpan, sticky=tk.E) 
		col = col + colSpan
		colSpan = 1
#		self.toggleDebugButton.grid(row=0, column=col, columnspan=colSpan, sticky=tk.E) 
		self.toggleRunOrClearDemoButton.grid(row=0, column=col, columnspan=colSpan, sticky=tk.E) 
#		for column, widget in enumerate((self.openDataFileButton, self.fileOffsetLabel, self.fileOffsetSpinbox, self.fileOffsetEntryLabel, self.fileOffsetEntry, self.toggleDebugButton)):
#			widget.grid(row=0, column=column+12, sticky=tk.W if widget != self.toggleDebugButton else tk.E)

#		self.fileOffsetEntryVariable = tk.StringVar()

		#######################
		# Second Row widgets
		#######################
		col = 0
		colSpan = 5
		self.originalCodeText.grid(row=1,column=0, columnspan=colSpan, sticky=tk.NSEW)
		col = col + colSpan
		colSpan = 1
		self.originalCodeTextVerticalScrollbar.grid(row=1,column=col, sticky=tk.NSEW)
		self.originalCodeText['yscrollcommand'] = self.originalCodeTextVerticalScrollbar.set
		
		col = col + colSpan
		colSpan = 5
		self.interpretedCodeText.grid(row=1,column=6, columnspan=5, sticky=tk.NSEW)
		self.interpretedCodeTextVerticalScrollbar.grid(row=1,column=11, sticky=tk.NSEW)
		self.interpretedCodeText['yscrollcommand'] = self.interpretedCodeTextVerticalScrollbar.set
		col = 12
		colSpan = 1
		self.addressColumnText.grid  (row=1, column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 6
		self.viewDataHexText.grid  (row=1, column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 2
		self.viewDataAsciiText.grid(row=1, column=col, columnspan=colSpan, sticky=tk.W)
		
		################################
		# Third Row widgets
		################################
		col = 0
		colSpan = 1
		self.CodeDataMeaningLabel.grid(row=2, rowspan=2, column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 11
		self.CodeDataMeaningText.grid(row=2, rowspan=2, column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.dataAddressStartLabel.grid(row=2, column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.dataAddressStartText.grid(row=2, column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.dataValueLELabel.grid(row=2,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 4
		self.dataValueLEText.grid(row=2,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.dataLengthLabel.grid(row=2,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.dataLengthText.grid(row=2,column=col, columnspan=colSpan, sticky=tk.W)

		################################
		# Fourth Row widgets
		################################
		col = 12
		colSpan = 1
		self.dataAddressEndLabel.grid(row=3, column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.dataAddressEndText.grid(row=3, column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1
		self.dataValueBELabel.grid(row=3,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 4
		self.dataValueBEText.grid(row=3,column=col, columnspan=colSpan, sticky=tk.W)
		col = col + colSpan
		colSpan = 1

		################################
		# Fifth Row widgets
		################################
		
		self.treeView.grid(row=4,column=0,columnspan=col+1, sticky=tk.NSEW)
		self.treeScroll.grid(row=4,column=col+2, sticky=tk.NSEW)
		self.treeView["columns"]=("1","2","3","4","5","6","7")
		self.treeView["height"]=7
		self.treeView.column("#0", width=100, anchor=tk.W)
		self.treeView.column("1", width=400, anchor=tk.W)
		self.treeView.column("2", width=200, anchor='c')
		self.treeView.column("3", width=100, anchor='c')
		self.treeView.column("4", width=100, anchor='c')
		self.treeView.column("5", width=200, anchor='c')
		self.treeView.column("6", width=150, anchor='c')
		self.treeView.column("7", width=150, anchor='c')

#		self.treeViewHeadings = ["Variable Name", "Data Type", "Addr Start", "Addr End", "Raw Hex Bytes", "Value (LE)", "Value (BE)"]
#		for c in range(len(self.treeViewHeadings)):

		# Special treatment for the Expand/Collapse function
		self.treeView.heading("#0", text="Expand/Collapse")					

		for c in range(len(treeViewHeadings)):
#			self.treeView.heading(STR(c+1), text=self.treeViewHeadings[c])
			self.treeView.heading(STR(c+1), text=treeViewHeadings[c])
			
		self.treeView['show'] = 'tree headings'				# Shows both the Tree icon and the Headings
#		self.treeView['show'] = 'headings'					# Hides the Expand/Collapse icon


		################################
		# Sixth Row widgets
		################################
		
		col = 0
		colSpan = 2
		self.toggleDebugButton.grid(row=5, column=col, columnspan=colSpan, sticky=tk.W) 
#		self.toggleRunOrClearDemoButton.grid(row=5, column=col, columnspan=colSpan, sticky=tk.W) 
		col = col + colSpan
		colSpan = 4
		'''
		self.toggleStructEndPaddingButton.grid(row=5, column=col, columnspan=colSpan, sticky=tk.W) 
		col = col + colSpan
		colSpan = 4
		'''
		self.toggleMapTypedefsTooButton.grid(row=5, column=col, columnspan=colSpan, sticky=tk.W) 
		
		
		self.frame.grid(row=0, column=0, sticky=tk.NSEW)

	def printCoordinates(self, eventOrigin):
		x = eventOrigin.x
		y = eventOrigin.y
		PRINT ("INFORMATION: Mouse click happened on Interpreted code window with pixel coordinates (x=",x,",y=",y,")" )
		currentCoordinates = self.interpretedCodeText.index(tk.CURRENT)
		PRINT ("Line.char currentCoordinates of last Mouse click =",currentCoordinates )

	def displayDataWindowFromOffset(self, newFileOffset):
		if newFileOffset < 0:
			return
		
		# When we change the displayed data window, which all Interpreted Code Window variables will get highlighted (based on cursor movement)
		# also changes. Hence, first we need to remove all those color tags.
		PRINT(self.interpretedCodeVariablesHighlightedStartEndCoordinates)
		for item in self.interpretedCodeVariablesHighlightedStartEndCoordinates:
			codeVarStart = item[0]
			codeVarEnd = item[1]
			self.interpretedCodeText.tag_remove("yellowbg", codeVarStart, codeVarEnd)
			
		currentWindowBaseNewValue = newFileOffset
		PRINT("Now going to set self.OK2reDisplayDataWindows = False")
		self.OK2reDisplayDataWindows = False
		self.fileOffsetSpinbox.delete(0,"end")
		PRINT("Now going to set self.OK2reDisplayDataWindows = True")
		self.OK2reDisplayDataWindows = True
		self.fileOffsetSpinbox.insert(0,currentWindowBaseNewValue)
		PRINT("After updating the self.fileOffsetSpinbox, self.fileOffsetSpinbox.get() =",self.fileOffsetSpinbox.get())
		if currentWindowBaseNewValue != int(self.fileOffsetSpinbox.get()):
			OUTPUT("ERROR - tried to set the offsetSpinbox to",currentWindowBaseNewValue,"but after the pasting, the value is",self.fileOffsetSpinbox.get())
		return

	# Find the line anchor that shows maximum number of variables corresponding to a data item in Hex or Ascii window
	def findLineAnchorForDoubleClickHexOrAscii(self, eventOrigin, HexOrAscii):
		if HexOrAscii == "Hex":
			widthPerByte = 3
			currentCoordinates = self.viewDataHexText.index(tk.CURRENT)
		elif HexOrAscii == "Ascii":
			widthPerByte = 1
			currentCoordinates = self.viewDataAsciiText.index(tk.CURRENT)
		else:
			OUTPUT("Invalid value of HexOrAscii =",STR(HexOrAscii))
			sys.exit()
		x = eventOrigin.x
		y = eventOrigin.y
		PRINT ("INFORMATION: Double click happened on", HexOrAscii,"window with pixel coordinates (x=",x,",y=",y,")" )
		PRINT ("Line.char currentCoordinates of last Mouse Double click in", HexOrAscii, "data window =",currentCoordinates )

		doubleClickLocationLineNum = int(currentCoordinates.split(".")[0])-1	# Remember that in Text widget the line # starts from 1, not 0
		doubleClickLocationCharNum = int(currentCoordinates.split(".")[1])
		
		if (0 <= doubleClickLocationLineNum < DISPLAY_BLOCK_HEIGHT) and (0 <= doubleClickLocationCharNum < DISPLAY_BLOCK_WIDTH*widthPerByte):
			PRINT("The double-click location at line #",doubleClickLocationLineNum,"and char #",doubleClickLocationCharNum,"is valid")
		else:
			errorMessage = "The double-click location at line #" + STR(doubleClickLocationLineNum) + "and char # "+ STR(doubleClickLocationCharNum) + " is invalid"
			errorRoutine(errorMessage)
			return False
			
		# From here, find the file Offset of the click location
		fileOffsetOfDoubleClickedLocation = fileDisplayOffset + doubleClickLocationLineNum * DISPLAY_BLOCK_WIDTH + integerDivision(doubleClickLocationCharNum,widthPerByte)
		PRINT("The double-click location at line #",doubleClickLocationLineNum,"and char #",doubleClickLocationCharNum,"corresponds to file offset of",fileOffsetOfDoubleClickedLocation)
		if not (fileDisplayOffset <= fileOffsetOfDoubleClickedLocation < fileDisplayOffset+BLOCK_SIZE):
			errorMessage = "The double-click location at line #" + STR(doubleClickLocationLineNum) + "and char # "+ STR(doubleClickLocationCharNum) + " is invalid because its corresponding file offset ("+STR(fileOffsetOfDoubleClickedLocation)+") is outside the file display range <"+STR(fileDisplayOffset)+","+STR(fileDisplayOffset+BLOCK_SIZE-1)+">"
			errorRoutine(errorMessage)
			return False
		
		# Now find out which all variables map to this fileOffsetOfDoubleClickedLocation
		variableIdsForThisDataLocation = []
		lineNumsForVariablesForThisDataLocation = []
		for item in sizeOffsets:
			if item[1] <= fileOffsetOfDoubleClickedLocation < item[1]+item[2]:
				tokenStartLineNum = tokenLocationLinesChars[variableDeclarations[item[0]][4]["globalTokenListIndex"]][0][0]
				variableName = variableDeclarations[item[0]][0]
				PRINT("variable",variableName,", which starts at line #",tokenStartLineNum,"map to this double-clicked data location")
				variableIdsForThisDataLocation.append(item[0])
				lineNumsForVariablesForThisDataLocation.append(tokenStartLineNum)

		lineNumsForVariablesForThisDataLocation.sort()
		PRINT("lineNumsForVariablesForThisDataLocation =\n")
		for item in lineNumsForVariablesForThisDataLocation:
			PRINT(item)
		# Find out the optimum window of displaying the mapped variables
		if not lineNumsForVariablesForThisDataLocation:
			return
		elif len(lineNumsForVariablesForThisDataLocation) == 1:
			PRINT("A single variable correspond to the data - no need to find out the optimum location")
			lineToAnchor = lineNumsForVariablesForThisDataLocation[0]
		else:
			# Here, when we use the term "variable", we only count those variables that correspond to the data location that has been double-clicked.
			# Here is the logic that we implement. if there is a single variable, we will show that.
			# However, if there are multiple variables that point to the same double-clicked data, then We want to maximize the number of such variables.
			# The problem is that, all these variables may not fit in the Interpreted code window, which can only show DISPLAY_BLOCK_HEIGHT lines at a time.
			# Hence, for every such variable, we try to find out if we start to show from that variable, how many other such variables we can also show.
			# Once we get this count, the highest guy wins. 
			# However, that still leaves the problem that there might be multiple such variables with identical show-count.
			# In such cases, to break the tie, we use the following criteria. We try to see whichever variable gives us the most "centered" feel.
			# Basically, we should try to have similar number of non-shown variables both BEFORE and AFTER the shown Interpreted window.
			PRINT("Many variables correspond to the double-clicked data - need to find out the optimum location")
			tab = []	# This table holds 4 entries < baseLine#, # non-visible variables before this window, # variables shown, # non-visible variables after this window>
			for i in range(len(lineNumsForVariablesForThisDataLocation)):
				baseLineNum = lineNumsForVariablesForThisDataLocation[i]
				#i is the number of variables missed before the window if we are starting to show from ith row of lineNumsForVariablesForThisDataLocation
				nonVisibleCountBeforeWindow = i
				visibleCount = 0
				nonVisibleCountAfterWindow = 0
				lastVisibleVariableLineNumForThisBaseLineNum = baseLineNum
				for j in range(len(lineNumsForVariablesForThisDataLocation[i+1:])):
					lineNum = lineNumsForVariablesForThisDataLocation[i+1+j]
					if lineNum < baseLineNum + DISPLAY_BLOCK_HEIGHT:
						visibleCount += 1
						lastVisibleVariableLineNumForThisBaseLineNum = lineNum
					else:
						nonVisibleCountAfterWindow += 1
				tab.append([baseLineNum, lastVisibleVariableLineNumForThisBaseLineNum, nonVisibleCountBeforeWindow, visibleCount, nonVisibleCountAfterWindow]) 
			# The -abs(x[2]-x[4]) term represents the assymetry between the before and after missed
			sortedTab = sorted(tab, key=lambda x: (x[3],-abs(x[2]-x[4])), reverse=True)
			PRINT("Unsorted tab = ",tab)
			PRINT("Sorted tab = ",sortedTab)
			lineToAnchor = integerDivision(sortedTab[0][0]+sortedTab[0][1],2)
			
		PRINT("Going to anchor line #",lineToAnchor)
		self.interpretedCodeText.see(STR(lineToAnchor+1)+".0")		# Here the screen line # starts from 1, not 0

	# When someone double-clicks on a colored data item, scroll the Interpreted code window to the place that maximizes the variables that correspond to that data
	def doubleClickAscii(self, eventOrigin):
		# If no variables have been mapped to some data, no use of this routine
		if not variableSelectedIndices or not sizeOffsets:
			return
		if not dataFileName or not dataFileSizeInBytes:
			return
		
		self.findLineAnchorForDoubleClickHexOrAscii(eventOrigin, "Ascii")


	# When someone double-clicks on a colored data item, scroll the Interpreted code window to the place that maximizes the variables that correspond to that data
	def doubleClickHex(self, eventOrigin):
		# If no variables have been mapped to some data, no use of this routine
		if not variableSelectedIndices or not sizeOffsets:
			return
		if not dataFileName or not dataFileSizeInBytes:
			return
		
		self.findLineAnchorForDoubleClickHexOrAscii(eventOrigin, "Hex")
		
	def doubleClickInterpreted(self, eventOrigin):
		# If no variables have been mapped to some data, no use of this routine
		if not variableSelectedIndices or not sizeOffsets:
			return
		if not dataFileName or not dataFileSizeInBytes:
			return
			
		x = eventOrigin.x
		y = eventOrigin.y
		PRINT ("INFORMATION: Double click happened on Interpreted code window with pixel coordinates (x=",x,",y=",y,")" )
		currentCoordinates = self.interpretedCodeText.index(tk.CURRENT)
		PRINT ("Line.char currentCoordinates of last Mouse Double click in the Interpreted code window =",currentCoordinates )

		doubleClickLocationLineNum = int(currentCoordinates.split(".")[0])-1	# Remember that in Text widget the line # starts from 1, not 0
		doubleClickLocationCharNum = int(currentCoordinates.split(".")[1])
		
		# Find index of the token on which the double-click happened. Remember that it need not be a token - it could be some whitespace too.
		# Also, it is possible that multiple tokens will get selected because there is no whitespace between them.
		doubleClickLocationTokenIndex = -100000
		doubleClickedTokenIndices = []
		i = 0
		for i in range(len(tokenLocationLinesChars)):
			if ((tokenLocationLinesChars[i][0][0] <= doubleClickLocationLineNum <= tokenLocationLinesChars[i][1][0]) and
				(tokenLocationLinesChars[i][0][1] <= doubleClickLocationCharNum <= tokenLocationLinesChars[i][1][1])):
				doubleClickedTokenIndices.append(i)
		if not doubleClickedTokenIndices:
			PRINT("The user has NOT double-clicked on any token")
			return True
		else:	
			# The user has indeed clicked on a token(s) (not space), but that may or may not be a variable.
			PRINT("The user has double-clicked on the following token indices =",doubleClickedTokenIndices)
			doubleClickedVariableIndices = []
			for doubleClickLocationTokenIndex in doubleClickedTokenIndices:
				k = 0
				while k in range(len(variableDeclarations)):
					item = variableDeclarations[k]
					if variableDeclarations[k][4]["variableId"] != k:
						errorMessage = "ERROR - wrong value of variableId - exiting"
						errorRoutine(errorMessage)
						return False
					elif (doubleClickLocationTokenIndex == item[4]["globalTokenListIndex"]):
						doubleClickedVariableIndices.append(k)
					k += 1
			
			if not doubleClickedVariableIndices:
				PRINT("Unfortunately, none of the tokens is a variable")
				return True
			else:
				doubleClickedSelectedVariableIndices = []	# The subset of doubleClickedVariableIndices, which are also mapped
				for doubleClickLocationVariableIndex in doubleClickedVariableIndices:
					# The user has indeed clicked on a variable, but that may or may not be selected for mapping.
					doubleClickLocationVariableName = variableDeclarations[doubleClickLocationVariableIndex][0]
					PRINT("The user clicked on a token which happens to be a variable <",doubleClickLocationVariableName,"> with variable index =",doubleClickLocationVariableIndex)
					if doubleClickLocationVariableIndex not in variableSelectedIndices:
						PRINT("Unfortunately, the variable",doubleClickLocationVariableName,"is not in variableSelectedIndices")
						PRINT("\nvariableSelectedIndices =",variableSelectedIndices)
					else:
						PRINT("Fortunately, token # ",doubleClickLocationTokenIndex,"which corresponds to",doubleClickLocationVariableIndex,"is indeed in variableSelectedIndices")
						doubleClickedSelectedVariableIndices.append(doubleClickLocationVariableIndex)

				if not doubleClickedSelectedVariableIndices:
					PRINT("Unfortunately, none of the variables",doubleClickedVariableIndices,"is not in variableSelectedIndices")
					return
				else:
					#if we have multiple candidates, choose the first one
					doubleClickLocationVariableIndex = doubleClickedSelectedVariableIndices[0]
					
					# Now find its absolute (NOT relative) offset and size
					itemFound = False
					for item in sizeOffsets:	# We do not know which order the sizeOffsets is sorted, hence need to find it
						if item[0] == doubleClickLocationVariableIndex:
							variableOffset =     item[1]	# Absolute value, not relative to dataLocationOffset
							variablelength =     item[2]
							selectedVariable = variableDeclarations[doubleClickLocationVariableIndex]
							itemFound = True
							break;
					if not itemFound:
						errorMessage("ERROR - Could not find the entry for variable id =",doubleClickLocationVariableIndex)
						errorRoutine(errorMessage)
						return False
					else:
						absoluteStart       = variableOffset
						absoluteEndExcluded = variableOffset + variablelength
						
						PRINT("Variable id =",doubleClickLocationVariableIndex,"has size",variablelength,", starts from relative offset of",HEX(variableOffset),"from dataLocationOffset =",HEX(dataLocationOffset))
						PRINT("Which means it starts from byte #",HEX(absoluteStart),"(included) and ends at byte #",HEX(absoluteEndExcluded),"(excluded)")
						
						currentWindowBaseOldValue = int(self.fileOffsetSpinbox.get())


						# If the variable is already being displayed, do nothing
						if variablelength >= BLOCK_SIZE:
							PRINT("Maximizing its display")
							currentWindowBaseNewValue = absoluteStart
						else:
							PRINT("Attempting to display the variable as close to the middle as possible")
							# Try to display the variable about right in the middle of the data display window
							currentWindowBaseNewValue = absoluteStart + integerDivision(variablelength,2)-integerDivision(BLOCK_SIZE,2)
							currentWindowBaseNewValue = 0 if currentWindowBaseNewValue < 0 else currentWindowBaseNewValue
							PRINT("The Display window needs to be redisplayed from byte #",HEX(currentWindowBaseNewValue),"to show the variable",HEX(doubleClickLocationVariableName),"right in the middle")
				
						if currentWindowBaseNewValue == currentWindowBaseOldValue:
							PRINT("No need to re-display")
							return
						else:
							PRINT("Going to re-display")
							PRINT("After redisplay, currentWindowBaseNewValue =",HEX(currentWindowBaseNewValue))
							self.displayDataWindowFromOffset(currentWindowBaseNewValue)
							return True
		

	# Anytime self.fileOffset changes, this gets called directly.
	# Anytime self.dataOffset changes, this gets called indirectly (via dataOffsetChange).
	def fileOffsetChange(self, *args):
		global fileDisplayOffset
	
		
		if self.OK2reDisplayDataWindows == False:
			PRINT("self.OK2reDisplayDataWindows is False - returning from fileOffsetChange()")
			return
		
		PRINT("Updating fileDisplayOffset to self.fileOffset.get() =",self.fileOffset.get())
		fileDisplayOffset = self.fileOffset.get()
			
		# Very important - when we change the data/file offset, which order the display routine for Code or Data gets executed matters.
		#
		# If the file offset changes, the displayBlock (the display window data) needs to be re-retrieved. The sizeOffsets etc. does not change.
		# So, in this case, first the Data and then the Code needs to be 
		# If the data offset changes, the displayBlock (the display window data) does NOT need to be re-retrieved. But sizeOffsets etc. changes.
		
		PRINT("Inside fileOffsetChange(), going to call self.updateDisplayBlock()")
		self.updateDisplayBlock()
		PRINT("Inside fileOffsetChange(), came back after calling self.updateDisplayBlock()")
		if sizeOffsets:
#			self.calculateSizeOffsets()
			self.performInterpretedCodeColoring()
#			self.populateDataMap()
		else:
			self.showDataBlock()
#		self.showDataBlock()	# Redundant?
#		self.populateDataMap()		# We need to call this ONLY after calling self.performInterpretedCodeColoring(), because it depends on populating the sizeOffsets[]

	# Anytime self.dataOffset changes, this gets called directly.
	def dataOffsetChange(self, *args):
		global dataLocationOffset
		PRINT("Previous value of dataLocationOffset =",dataLocationOffset)
		dataLocationOffset = self.dataOffset.get()
		PRINT("Current value of dataLocationOffset =",dataLocationOffset)
		self.calculateSizeOffsets()
		self.fileOffsetChange()
		self.populateDataMap()
		
	def dataPageUp(self, *args):
		if not dataFileName or not dataFileSizeInBytes:
			return
		PRINT("Page Up")
		currentWindowBaseOldValue = int(self.fileOffsetSpinbox.get())
		PRINT("Current self.fileOffsetSpinbox.get() =",currentWindowBaseOldValue)
		currentWindowBaseNewValue = currentWindowBaseOldValue - BLOCK_SIZE if currentWindowBaseOldValue - BLOCK_SIZE >= 0 else 0
		PRINT("After Page Up, currentWindowBaseNewValue =",currentWindowBaseNewValue)
		self.displayDataWindowFromOffset(currentWindowBaseNewValue)
		return True
		
	def dataPageDown(self, *args):
		if not dataFileName or not dataFileSizeInBytes:
			return
		PRINT("Page Down")
		currentWindowBaseOldValue = int(self.fileOffsetSpinbox.get())
		PRINT("Current self.fileOffsetSpinbox.get() =",currentWindowBaseOldValue)
		currentWindowBaseNewValue = currentWindowBaseOldValue+BLOCK_SIZE if currentWindowBaseOldValue+BLOCK_SIZE <= dataFileSizeInBytes-1 else dataFileSizeInBytes - BLOCK_SIZE
		PRINT("After Page Down, setting currentWindowBaseNewValue =",currentWindowBaseNewValue)
		self.displayDataWindowFromOffset(currentWindowBaseNewValue)
		return True
		
	def create_bindings(self):
		for keypress in ("<Control-o>", "<Alt-o>"):
			self.parent.bind(keypress, self.openDataFileDialogue)
		for keypress in ("<Control-q>", "<Alt-q>", "<Escape>"):
			self.parent.bind(keypress, self.quit)
		self.parent.bind("<Alt-f>", lambda *args: self.fileOffsetSpinbox.focus())
		self.interpretedCodeText.bind("<Button 1>",self.printCoordinates)
		
		self.interpretedCodeText.bind("<Double 1>",self.doubleClickInterpreted)	 
		self.viewDataHexText.bind("<Double 1>",self.doubleClickHex)	 
		self.viewDataAsciiText.bind("<Double 1>",self.doubleClickAscii)	 
		
		# When the data offset changes, the unraveled data should also change
		for variable in (self.dataOffset,):
			variable.trace_variable("w", self.dataOffsetChange)
			
		# When the file offset changes, the unraveled data should NOT change
		for variable in (self.fileOffset,):
			variable.trace_variable("w", self.fileOffsetChange)
		
		self.addressColumnText.bind("<Prior>",self.dataPageUp)
		self.viewDataHexText.bind("<Prior>",self.dataPageUp)
		self.viewDataAsciiText.bind("<Prior>",self.dataPageUp)

		self.addressColumnText.bind("<Next>",self.dataPageDown)
		self.viewDataHexText.bind("<Next>",self.dataPageDown)
		self.viewDataAsciiText.bind("<Next>",self.dataPageDown)
		

	def getDataCoordinates(self, dataByteStartOffset, dataByteEndOffset):
		# These two offsets below describe the displayed window range (has nothing to do with the specific data)
		# The Pythonic way: "START" is included, "END" is not included
		firstByteDisplayedOffset = fileDisplayOffset	# The file offset of first byte displayed on the window
		lastByteDisplayedOffsetPlusOne = fileDisplayOffset + BLOCK_SIZE	# The file offset of first byte after firstByteDisplayedOffset NOT displayed on the window
																			
		if dataByteStartOffset > dataByteEndOffset:
			PRINT ("ERROR: dataByteStartOffset =",dataByteStartOffset, "is greater than dataByteEndOffset =", dataByteEndOffset )
			errorMessage = "ERROR: dataByteStartOffset =" + str(dataByteStartOffset) + "is greater than dataByteEndOffset =" + str(dataByteEndOffset)+" !!!"
			errorRoutine(errorMessage)
			return False
#		elif dataByteStartOffset < firstByteDisplayedOffset and dataByteEndOffset > lastByteDisplayedOffsetPlusOne:		# I think this is wrong
		elif dataByteEndOffset < firstByteDisplayedOffset or  dataByteStartOffset >= lastByteDisplayedOffsetPlusOne:
			errorMessage = "ERROR: Input byte <start,end> pair = <"+STR(dataByteStartOffset)+" ,"+ STR(dataByteEndOffset)+"> is outside the display window <"+STR(firstByteDisplayedOffset)+" ,"+STR(lastByteDisplayedOffsetPlusOne)+"(excluded)>"
			PRINT(errorMessage)
			return False	# TO-DO: Should we change it to False or blank?
		
		PRINT ("Data byte range <",dataByteStartOffset, ",", dataByteEndOffset,"> is displayable within current display window of <",firstByteDisplayedOffset,",", lastByteDisplayedOffsetPlusOne,"(excluded)>")

		startOffset = firstByteDisplayedOffset if dataByteStartOffset < firstByteDisplayedOffset else dataByteStartOffset
		endOffset = lastByteDisplayedOffsetPlusOne if dataByteEndOffset > lastByteDisplayedOffsetPlusOne else dataByteEndOffset
		

		# Find the start and end location in the Hex and Ascii Windows. Remeber, conforming to the Pythonic way, the Start coordinate is included, the End coordiate is not
		startLineNum = integerDivision((startOffset-firstByteDisplayedOffset),DISPLAY_BLOCK_WIDTH)
		startCharNumAscii = (startOffset-firstByteDisplayedOffset)%DISPLAY_BLOCK_WIDTH
		startCharNumHex = startCharNumAscii * 3
		endLineNum = integerDivision((endOffset-firstByteDisplayedOffset),DISPLAY_BLOCK_WIDTH)
		endCharNumAscii = (endOffset-firstByteDisplayedOffset)%DISPLAY_BLOCK_WIDTH
		endCharNumHex = endCharNumAscii * 3 
		startStrHex = str(startLineNum+1) + "." + str(startCharNumHex)			# Recall that on Text line number starts from 1, not 0
		endStrHex = str(endLineNum+1) + "." + str(endCharNumHex)				# Recall that on Text line number starts from 1, not 0
		startStrAscii = str(startLineNum+1) + "." + str(startCharNumAscii)		# Recall that on Text line number starts from 1, not 0
		endStrAscii = str(endLineNum+1) + "." + str(endCharNumAscii)			# Recall that on Text line number starts from 1, not 0
		PRINT ("Hex coordinates are",startStrHex,"(inlcuded) and ends at", endStrHex,"(NOT inlcuded)" )
		PRINT ("Ascii coordinates are",startStrAscii,"(inlcuded) and ends at", endStrAscii,"(NOT inlcuded)" )
		return [[startStrHex,endStrHex],[startStrAscii,endStrAscii]]



	############################################################################################################################
	# The updateDataBlock() populates a global variable-size dataBlock variable. It does not return the dataBlock.
	############################################################################################################################
	def updateDataBlock(self):
		global dataBlock
		if not dataFileName:
			return False

		PRINT("Entered updateDataBlock(), currently self.fileOffset = ",self.fileOffset.get(), "self.dataOffset = ",self.dataOffset.get())
		# If dataLocationOffsetEntryVariable is blank, set it to zero
		PRINT("Inside updateDataBlock(), going to zeroize self.dataOffset if blank")
		try:
			PRINT("Inside updateDataBlock(), currently self.dataOffset.get() = <",self.dataOffset.get(),">")
			if STR(self.dataOffset.get()).strip() == '':
				PRINT ("WARNING - Blank self.dataOffset!!" )
				PRINT("Inside updateDataBlock(), currently self.dataOffset.get() = <",self.dataOffset.get(),"> going to perform self.dataOffset.set(0)")
				self.dataOffset.set(0)
				PRINT("Inside updateDataBlock(), just performed self.dataOffset.set(0), now self.dataOffset.get() =",self.dataOffset.get())
		except ValueError: 
			PRINT ("WARNING - Blank self.dataOffset - setting it to 0!!" )
			PRINT("Inside updateDataBlock(), going to perform self.dataOffset.set(0) for ValueError")
			self.dataOffset.set(0)
			PRINT("Inside updateDataBlock(), just performed self.dataOffset.set(0) for ValueError")
			PRINT("Inside updateDataBlock(), zeroized self.dataOffset if it was blank")
			
		dataBlock = readBytesFromFile(dataLocationOffset, totalBytesToReadFromDataFile)

	############################################################################################################################
	# The updateDisplayBlock() populates a global fixed-size displayBlock variable. It does not return the displayBlock.
	############################################################################################################################
	def updateDisplayBlock(self):
		global displayBlock
		if (not dataFileName) or (dataFileName == None):
			return False

		PRINT("Entered updateDisplayBlock(), currently self.fileOffset = ",self.fileOffset.get(), "self.dataOffset = ",self.dataOffset.get())
			
		# If dataFileOffset is blank, set it to zero
		PRINT("Inside updateDisplayBlock(), going to zeroize self.fileOffset if blank")
		try:
			PRINT("Inside updateDisplayBlock(), currently self.fileOffset.get() = <",self.fileOffset.get(),">")
			if STR(self.fileOffset.get()).strip() == '':
#				if not self.fileOffset.get():	# <==== HUGE BUG! DO not use this. Keeping this to warn you.
				PRINT ("WARNING - Blank self.fileOffset!!" )
				PRINT("Inside updateDisplayBlock(), currently self.fileOffset.get() = <",self.fileOffset.get(),">. Now going to perform self.fileOffset.set(0)")
				self.fileOffset.set(0)
				PRINT("Inside updateDisplayBlock(), just performed self.fileOffset.set(0), now self.fileOffset.get()", self.fileOffset.get())
		except ValueError: 
			PRINT ("WARNING - Blank self.fileOffset - setting it to 0!!" )
			PRINT("Inside updateDisplayBlock(), going to perform self.fileOffset.set(0) for ValueError")
			self.fileOffset.set(0)
			PRINT("Inside updateDisplayBlock(), just performed self.fileOffset.set(0) for ValueError")
		PRINT("Inside updateDisplayBlock(), zeroized self.fileOffset if it was blank")
		
		displayBlock = readBytesFromFile(fileDisplayOffset, BLOCK_SIZE)
			
		PRINT("Leaving updateDisplayBlock(), currently self.fileOffset = ",self.fileOffset.get(), "self.dataOffset = ",self.dataOffset.get())
				
		return True	

	###############################################################################################################################
	# The biggest routine
	###############################################################################################################################

	def showDataBlock(self, *args):
		
		if not dataFileName:
			return False

		PRINT("\nEntered showDataBlock()")
			
		self.addressColumnText.delete("1.0", "end")
		self.viewDataHexText.delete("1.0", "end")
		self.viewDataAsciiText.delete("1.0", "end")
		
		self.interpretedCodeVariablesHighlightedStartEndCoordinates = []
		
		PRINT("Inside showDataBlock(), deleted Address/Hex/Ascii windows")
		
		PRINT ("\n"*3,"=="*50,"\n Inside showDataBlock(), for data Offset =",dataLocationOffset,"File Offset =",fileDisplayOffset,"\n","=="*50,"\n"*3)

		self.updateDisplayBlock()

		
		# Populate the Address column
		
		startAddress = fileDisplayOffset
		for rowNum in range(DISPLAY_BLOCK_HEIGHT):
			address = startAddress + rowNum * DISPLAY_BLOCK_WIDTH
			addressStr = "0x{:010X} ".format(address)+ ("\n" if rowNum < DISPLAY_BLOCK_HEIGHT-1 else "")
			printAddress = str(rowNum+1)+"."+"0"
			PRINT ("Row ",rowNum,". Address = ",addressStr )
			self.addressColumnText.insert("end",addressStr)

		# Populate the Display window row by row, without adding any tags (no color or cursor movement)
		
		rows = [displayBlock[i:i + DISPLAY_BLOCK_WIDTH] for i in range(0, len(displayBlock), DISPLAY_BLOCK_WIDTH)]
		
		if len(rows) > DISPLAY_BLOCK_HEIGHT:
			PRINT("ERROR in showDataBlock() - len(rows) =", len(rows), ", which is  > DISPLAY_BLOCK_HEIGHT =", DISPLAY_BLOCK_HEIGHT)
			sys.exit()
			
		for rowNum in range(len(rows)):
			row = rows[rowNum]
			rowStartOffset =  DISPLAY_BLOCK_WIDTH * rowNum
			fileOffset = fileDisplayOffset + rowStartOffset
			PRINT ("Now printing row #", rowNum, "starting from original offset",fileDisplayOffset," + current Offset ", rowStartOffset," = fileOffset",fileOffset )
			self.showIndividualLine(row,fileOffset)	# For both Hex and Ascii windows
			# There should be a newline at the end of every line. However, we cannot put this responsibility in showIndividualLine() because the last line should not have it,
			# and the showIndividualLine() cannot know which line is the last line. So, we add it explicitly outside.
			if rowNum < len(rows)-1:
				self.viewDataHexText.insert("end", "\n")
				self.viewDataAsciiText.insert("end", "\n")

		# Now add the color and cursor-movement by adding tags
		
		# First get the current window (from which byte to which byte of the file is displayed)
		firstByteDisplayedOffset = fileDisplayOffset
		lastByteDisplayedOffsetPlusOne  = fileDisplayOffset + BLOCK_SIZE

		PRINT ("Current value of dataLocationOffset =",dataLocationOffset,"firstByteDisplayedOffset =",firstByteDisplayedOffset,"lastByteDisplayedOffsetPlusOne =",lastByteDisplayedOffsetPlusOne)
		dumpDetailsForDebug()
		
		# The problem is that there is no guarantee that if all the mapped data will fit in the current window. It may spill over multiple windows.
		# So, we check if anything in the current window needs to be colored by the following logic.
		# If the first or last member of dataOffsets[] (after adding dataLocationOffset) falls within the <firstByteDisplayedOffset,lastByteDisplayedOffsetPlusOne>,
		# Then we know that there is SOMETHING to color. 
		
		# TO-DO: However, when we get the actual data value, we need to get the right data:
		
		
		# There could be only two possibilities where we display any data coloring (in other cases, no data coloring is needed)
		# Either the data starts/ends within the Display window, or it starts before AND ends after the current display window.
		# We keep this explicit check for efficiency. We are going to apply the same condition for each of the colored items, but if we know that none of them would match,
		# there is no point doing this check anyway (potentially there could be thousands of fields to color).
		if sizeOffsets and  ( (firstByteDisplayedOffset <= dataLocationOffset 								 < lastByteDisplayedOffsetPlusOne) or	# First byte within window
							  (firstByteDisplayedOffset <= dataLocationOffset+totalBytesToReadFromDataFile-1 < lastByteDisplayedOffsetPlusOne) or	# Last byte within window
							  ((dataLocationOffset<firstByteDisplayedOffset) and (dataLocationOffset+totalBytesToReadFromDataFile >= lastByteDisplayedOffsetPlusOne))):
					
			tagIndex = -1 		# Error value
			for j in range(len(sizeOffsets)):
				try:
					# Check if the tag # j applies to this.
					if ((firstByteDisplayedOffset <= (sizeOffsets[j][1]					 ) <= lastByteDisplayedOffsetPlusOne) or 
						(firstByteDisplayedOffset <= (sizeOffsets[j][1]+sizeOffsets[j][2]) <= lastByteDisplayedOffsetPlusOne) or
						((sizeOffsets[j][1] < firstByteDisplayedOffset) and (lastByteDisplayedOffsetPlusOne < sizeOffsets[j][1]+sizeOffsets[j][2]))): # This is data to be colored differently
						
						tagIndex = j
						
						# Gather the necessary data about the variables
						variableName = variableDeclarations[sizeOffsets[j][0]][0]
						variableDescription = variableDeclarations[sizeOffsets[j][0]][4]["description"]
						signedOrUnsigned = variableDeclarations[sizeOffsets[j][0]][4]["signedOrUnsigned"]
						datatype = variableDeclarations[sizeOffsets[j][0]][4]["datatype"]
						isArray = variableDeclarations[sizeOffsets[j][0]][4]["isArray"]
						arrayDimensions = variableDeclarations[sizeOffsets[j][0]][4]["arrayDimensions"] if isArray else []
						arrayElementSize = variableDeclarations[sizeOffsets[j][0]][4]["arrayElementSize"] if isArray else 0
						isBitField = variableDeclarations[sizeOffsets[j][0]][4]["isBitField"]

						# For the Interpreted code window, find out the locations of the variable names (to which the tags would apply)
						tokenStartLineNum = tokenLocationLinesChars[variableDeclarations[sizeOffsets[j][0]][4]["globalTokenListIndex"]][0][0]
						tokenStartCharNum = tokenLocationLinesChars[variableDeclarations[sizeOffsets[j][0]][4]["globalTokenListIndex"]][0][1]
						tokenEndLineNum = tokenLocationLinesChars[variableDeclarations[sizeOffsets[j][0]][4]["globalTokenListIndex"]][1][0]
						tokenEndCharNum = tokenLocationLinesChars[variableDeclarations[sizeOffsets[j][0]][4]["globalTokenListIndex"]][1][1]
						strCodeWindowVariableStart = str(tokenStartLineNum+1)+"."+str(tokenStartCharNum)		# Remember that on Text the line number starts from 1, not 0
						strCodeWindowVariableEnd   = str(tokenEndLineNum  +1)+"."+str(tokenEndCharNum+1)		# Remember that on Text the line number starts from 1, not 0


						#Add the start and end coordinates to this array. These are pretty much ALL the coordinates of the selected 
						self.interpretedCodeVariablesHighlightedStartEndCoordinates.append([strCodeWindowVariableStart,strCodeWindowVariableEnd])


						PRINT ("Currently handling",variableDescription )
						if isArray != True and isArray != False:
							OUTPUT ("Uh-Oh - isArray's value is",isArray )
							sys.exit()
						
						# If this is an array, get the actions specific to individual array elements
						
						if isArray:
						
							################################
							#     Handle Array variables   #
							################################
							
							PRINT (variableName, " is an array of dimensions ", arrayDimensions )
							totalNumberOfArrayElements = listItemsProduct(arrayDimensions)
							if isBitField:
								errorMessage = "ERROR: Array "+ variableName + " cannot be bitfield"
								errorRoutine(errorMessage)
								return False
							elif totalNumberOfArrayElements == False:
								errorMessage = "ERROR: Array dimensions must be positive integers, while for "+ variableName +" arrayDimensions =" + STR(arrayDimensions)
								errorRoutine(errorMessage)
								return False
							elif not isinstance(self.colorTagsData[j], list):
								PRINT ("ERROR: self.colorTagsData[",j,"] =",self.colorTagsData[j],"is not a list" )
								errorMessage = "ERROR: self.colorTagsData["+STR(j)+"] = "+STR(self.colorTagsData[j])+" is not a list"
								errorRoutine(errorMessage)
								return False
							elif totalNumberOfArrayElements != len(self.colorTagsData[j]):
								PRINT ("ERROR: self.colorTagsData[",j,"] =",self.colorTagsData[j],"is a list of size",len(self.colorTagsData[j]),"while totalNumberOfArrayElements=",totalNumberOfArrayElements,"for arrayDimensions =",arrayDimensions )
								return False
							

							# Verify that the size of the total variable (or array) indeed matches the size offsets
							dataTypeSize = getDatatypeSize(datatype)
							if arrayElementSize != dataTypeSize:
								errorMessage = "ERROR: For j="+STR(j)+", variable = <"+variableName+">, arrayElementSize = "+STR(arrayElementSize)+"does not match datatype <"+datatype+"> size ("+STR(dataTypeSize)
								errorRoutine(errorMessage)
								return False
							else:
								expectedTotalArraySizeInBytes = totalNumberOfArrayElements *  arrayElementSize
								if expectedTotalArraySizeInBytes != sizeOffsets[j][2]:
									errorMessage = "ERROR: For j="+STR(j)+"sizeOffsets[j][2]="+STR(sizeOffsets[j][2])+"does not match datatype <"+datatype+"> size ("+STR(dataTypeSize)+") X getDatatypeSize("+datatype+") x totalNumberOfArrayElements ("+STR(totalNumberOfArrayElements)+") = "+STR(expectedTotalArraySizeInBytes)
									errorRoutine(errorMessage)
									return False
								else:
									for position in range(totalNumberOfArrayElements):	# e.g. in an array[2][2], position 0 means array[0][0] and position 3 means array[1][1]
										PRINT ("="*30,"\nHandling position = ",position,"in array dimension",arrayDimensions,"\n","="*30 )
										byteOffsetWithinArrayVariable = position * arrayElementSize
										arrayIndices = calculateArrayIndicesFromPosition(arrayDimensions, position)
										arrayIndicesCStyle = ""	# We convert the [i,j,k] to C-style [i][j][k]
										for item in arrayIndices:
											arrayIndicesCStyle += "["+STR(item)+"]"
										arrayElementIndexDescription = STR(variableName)+arrayIndicesCStyle+" (element # "+STR(position)+")"

										arrayElementByteStart = sizeOffsets[j][1] + byteOffsetWithinArrayVariable					 # Inclusive
										arrayElementByteEnd   = sizeOffsets[j][1] + byteOffsetWithinArrayVariable + arrayElementSize # Not inclusive

										if ((firstByteDisplayedOffset <= arrayElementByteStart < lastByteDisplayedOffsetPlusOne) or 
											(firstByteDisplayedOffset <  arrayElementByteEnd   <= lastByteDisplayedOffsetPlusOne)): # This is data to be colored differently

											getDataCoordinatesResult = self.getDataCoordinates( arrayElementByteStart, arrayElementByteEnd )
											if getDataCoordinatesResult == False:
												errorMessage = "ERROR: while calling routine getDataCoordinates(arrayElementByteStart=%d, arrayElementByteEnd=%d) - for data item # j=<%d>, %s -- exiting!"%(arrayElementByteStart, arrayElementByteEnd,j,arrayElementIndexDescription)
												errorRoutine(errorMessage)
												dumpDetailsForDebug()
												OUTPUT ("This should never happen since we already checked that it overlaps with the display window")
												sys.exit()
												return False
											else:
												printMessage = "For data item # j=<%d>, %s, getDataCoordinates(dataByteStartOffset=%d, dataByteEndOffset=%d) = %s!"%(j, arrayElementIndexDescription, arrayElementByteStart, arrayElementByteEnd,STR(getDataCoordinatesResult))
												PRINT (printMessage )
												
												startStrHex   = getDataCoordinatesResult[0][0]
												endStrHex     = getDataCoordinatesResult[0][1]
												startStrAscii = getDataCoordinatesResult[1][0]
												endStrAscii   = getDataCoordinatesResult[1][1]
												
												# We can mention the line.char of the end position of the tag, or we can just say line.char of the start position of the tag + size[j] characters
												startEndStrHex   = startStrHex   + " + " + str(arrayElementSize*3) + " chars"
												startEndStrAscii = startStrAscii + " + " + str(arrayElementSize)   + " chars"


												# We do NOT get the data from the displayed Hex or Ascii window. We get it from the original File.
												# This the actual file offset the variable starts from (this could actually be before the current frame)
												actualDataAddrStart = "0x{:010X}".format(arrayElementByteStart)
												actualDataAddrEnd = "0x{:010X}".format(arrayElementByteStart+arrayElementSize-1)	# This byte is for display, hence inclusive
												dataLengthValue = str(arrayElementSize)+" byte" + ("s" if arrayElementSize > 1 else "")
												# The displayBlock already is showing the self.fileOffset as offset 0, so need to take care of that
												
												if arrayElementByteStart-fileDisplayOffset < 0 or arrayElementByteEnd-fileDisplayOffset >= BLOCK_SIZE:
													valueBytes = readBytesFromFile(arrayElementByteStart, arrayElementSize)
													if len(valueBytes) < arrayElementSize:
														break
												else:
													valueBytes = displayBlock[ arrayElementByteStart-fileDisplayOffset : arrayElementByteEnd-fileDisplayOffset ]
												
												
												
												# get the Big endian and Little endian values
												valueBE = ""
												valueLE = ""
												if datatype in getDictKeyList(structuresAndUnionsDictionary):
													pass
												elif datatype in getDictKeyList(typedefs) and isinstance(typedefs[datatype],list) and len(typedefs[datatype])==2 and (typedefs[datatype][0] in ("struct","union")):
													pass
												elif (len(valueBytes) in (1,2,4,8)) and (signedOrUnsigned in ("signed","unsigned")):
													valueBE = calculateInternalValue(valueBytes, BIG_ENDIAN, datatype, signedOrUnsigned) 
													valueLE = calculateInternalValue(valueBytes, LITTLE_ENDIAN, datatype, signedOrUnsigned)
												else:
													PRINT ("WARNING - unhandled case - need to code" )
												
												valueBEStr = str(valueBE)
												valueLEStr = str(valueLE)
							
												variableDescriptionArrayElement = arrayElementIndexDescription + ", where " + variableDescription
												PRINT ("\n"*2,"==="*50,"\ndataLocationOffset =",dataLocationOffset,"File Offset =",fileDisplayOffset,"for Array variable #",j,"= ",variableDeclarations[sizeOffsets[j][0]][0],arrayElementIndexDescription,"located between address",actualDataAddrStart,"and",actualDataAddrEnd,"valueBytes=0x",valueBytes,"translates into",str(valueLE) + " (LE), " + str(valueBE) + " (BE)","\n","==="*50 )
												for byteIndex in range(len(valueBytes)): 
													PRINT ("valueBytes[",byteIndex,"] = ",ORD(valueBytes[byteIndex]) )

												# Apply the tag to the Hex window
												PRINT ("Going to apply the tag",self.colorTagsData[j][position],"in Hex window from",startStrHex,"to", endStrHex, "(",startEndStrHex,") for Array variable",j,variableDeclarations[sizeOffsets[j][0]][0],", with variableDescription =",variableDescriptionArrayElement )
												self.viewDataHexText.tag_add(self.colorTagsData[j][position], startStrHex, endStrHex)
#												self.viewDataHexText.tag_add(self.colorTagsData[j][position], startStrHex, startEndStrHex)

												# This is no real list. We just create a fake list so that individual list items (each one is a statement) gets executed.
												# This is a dirty hack, but I don't know how to do it the pythonic way to make multi-statement Lambda functions.
												self.viewDataHexText.tag_bind(self.colorTagsData[j][position], "<Enter>", 
													lambda event, textValue=variableDescriptionArrayElement, addrValueStart=actualDataAddrStart, addrValueEnd=actualDataAddrEnd, 
													lengthValue=dataLengthValue, dataValueLEValue=valueLEStr, dataValueBEValue=valueBEStr, 
													startStrHexValue=startStrHex, endStrHexValue=endStrHex, startStrAsciiValue=startStrAscii, endStrAsciiValue=endStrAscii, 
													codeVarStart=strCodeWindowVariableStart, codeVarEnd=strCodeWindowVariableEnd: 
													[self.CodeDataMeaningText.configure(text=textValue), 
													 self.dataAddressStartText.configure(text=addrValueStart),
													 self.dataAddressEndText.configure(text=addrValueEnd),			# This address is INCLUDED. Which means, the field ends here.
													 self.dataLengthText.configure(text=lengthValue),
													 self.dataValueLEText.configure(text=dataValueLEValue), 
													 self.dataValueBEText.configure(text=dataValueBEValue), 
													 self.viewDataHexText.tag_add("yellowbg", startStrHexValue, endStrHexValue),
													 self.viewDataAsciiText.tag_add("yellowbg", startStrAsciiValue, endStrAsciiValue),
													 self.interpretedCodeText.tag_add("yellowbg", codeVarStart, codeVarEnd)])
													 
												self.viewDataHexText.tag_bind (self.colorTagsData[j][position], "<Leave>", 
													lambda event, textValue="", startStrHexValue=startStrHex, endStrHexValue=endStrHex, startStrAsciiValue=startStrAscii, endStrAsciiValue=endStrAscii, 
													codeVarStart=strCodeWindowVariableStart, codeVarEnd=strCodeWindowVariableEnd : 
													[self.CodeDataMeaningText.configure(text=textValue), 
													 self.dataAddressStartText.configure(text=""), 
													 self.dataAddressEndText.configure(text=""),
													 self.dataLengthText.configure(text=""), 
													 self.dataValueLEText.configure(text=""), 
													 self.dataValueBEText.configure(text=""), 
													 self.viewDataHexText.tag_remove("yellowbg", startStrHexValue, endStrHexValue),
													 self.viewDataAsciiText.tag_remove("yellowbg", startStrAsciiValue, endStrAsciiValue),
													 self.interpretedCodeText.tag_remove("yellowbg", codeVarStart, codeVarEnd)])

												# Apply the tag for the ASCII window
												
												PRINT ("Going to apply the tag",self.colorTagsData[j][position],"in ASCII window from",startStrAscii,"to", endStrAscii, "(",startEndStrAscii,") for Array variable",j,variableDeclarations[sizeOffsets[j][0]][0],", with variableDescription =",variableDescriptionArrayElement )
												self.viewDataAsciiText.tag_add (self.colorTagsData[j][position], startStrAscii, endStrAscii)
#												self.viewDataAsciiText.tag_add (self.colorTagsData[j][position], startStrAscii, startEndStrAscii)

												self.viewDataAsciiText.tag_bind(self.colorTagsData[j][position], "<Enter>", 
													lambda event, textValue=variableDescriptionArrayElement, addrValueStart=actualDataAddrStart, addrValueEnd=actualDataAddrEnd, 
													lengthValue=dataLengthValue, dataValueLEValue=valueLEStr, dataValueBEValue=valueBEStr, 
													startStrHexValue=startStrHex, endStrHexValue=endStrHex, startStrAsciiValue=startStrAscii, endStrAsciiValue=endStrAscii, 
													codeVarStart=strCodeWindowVariableStart, codeVarEnd=strCodeWindowVariableEnd : 
													[self.CodeDataMeaningText.configure(text=textValue),
													 self.dataAddressStartText.configure(text=addrValueStart),
													 self.dataAddressEndText.configure(text=addrValueEnd),
													 self.dataLengthText.configure(text=lengthValue),
													 self.dataValueLEText.configure(text=dataValueLEValue), 
													 self.dataValueBEText.configure(text=dataValueBEValue), 
													 self.viewDataHexText.tag_add("yellowbg", startStrHexValue, endStrHexValue),
													 self.viewDataAsciiText.tag_add("yellowbg", startStrAsciiValue, endStrAsciiValue),
													 self.interpretedCodeText.tag_add("yellowbg", codeVarStart, codeVarEnd),
													 self.interpretedCodeText.tag_add("yellowbg", codeVarStart, codeVarEnd)])
													 
												self.viewDataAsciiText.tag_bind(self.colorTagsData[j][position], "<Leave>", 
													lambda event, textValue="", startStrHexValue=startStrHex, endStrHexValue=endStrHex, startStrAsciiValue=startStrAscii, endStrAsciiValue=endStrAscii, 
													codeVarStart=strCodeWindowVariableStart, codeVarEnd=strCodeWindowVariableEnd  : 
													[self.CodeDataMeaningText.configure(text=textValue),
													 self.dataAddressStartText.configure(text=""), 
													 self.dataAddressEndText.configure(text=""), 
													 self.dataLengthText.configure(text=""), 
													 self.dataValueLEText.configure(text=""), 
													 self.dataValueBEText.configure(text=""), 
													 self.viewDataHexText.tag_remove("yellowbg", startStrHexValue, endStrHexValue),
													 self.viewDataAsciiText.tag_remove("yellowbg", startStrAsciiValue, endStrAsciiValue),
													 self.interpretedCodeText.tag_remove("yellowbg", codeVarStart, codeVarEnd)])
													 
												tags = (self.colorTagsData[tagIndex][position],)
						else:
						
							################################
							# Handle non-Array variables
							################################

							
							PRINT (variableName, "is NOT an array" )
							
							getDataCoordinatesResult = self.getDataCoordinates( (sizeOffsets[j][1]), (sizeOffsets[j][1]+sizeOffsets[j][2]) )
							if getDataCoordinatesResult == False:
								continue	# This tag is not applicable
							else:
								startStrHex   	= getDataCoordinatesResult[0][0] 
								endStrHex   	= getDataCoordinatesResult[0][1]
								startStrAscii 	= getDataCoordinatesResult[1][0] 
								endStrAscii  	= getDataCoordinatesResult[1][1]


							# We can mention the line.char of the end position of the tag, or we can just say line.char of the start position of the tag + size[j] characters
							startEndStrHex   = startStrHex   + " + " + str(sizeOffsets[j][2]*3) + " chars"
							startEndStrAscii = startStrAscii + " + " + str(sizeOffsets[j][2])   + " chars"
							
							# We do NOT get the data from the displayed Hex or Ascii window. We get it from the original File.
							# This the actual file offset the variable starts from (this could actually be before the current frame)
							actualDataAddrStart = "0x{:010X}".format(sizeOffsets[j][1])
							actualDataAddrEnd   = "0x{:010X}".format(sizeOffsets[j][1]+sizeOffsets[j][2]-1)	# This byte is INCLUDED
							dataLengthValue = STR(sizeOffsets[j][2])+" byte" + ("s" if sizeOffsets[j][2] > 1 else "")
							'''
							if isBitField:
								bitFieldInfo = variableDeclarations[sizeOffsets[j][0]][4]["bitFieldInfo"]
								actualDataAddrStart = "0x{:X}".format(sizeOffsets[j][1] + 
														integerDivision( bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"],BITS_IN_BYTE)) +
														"." + STR(bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"]%BITS_IN_BYTE) + " (LE)"
								actualDataAddrEnd   = "0x{:X}".format(sizeOffsets[j][1] +				# This byte is INCLUDED
														integerDivision( bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"],BITS_IN_BYTE)) +
														"." + STR(bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"]%BITS_IN_BYTE) + " (LE)"
								dataLengthValue = STR(variableDeclarations[sizeOffsets[j][0]][4]["bitFieldWidth"]) + " bits"
							'''
							
							notEnoughDataToMap = False

							# The displayBlock already is showing the self.fileOffset as offset 0, so need to take care of that
							numBytesToRead =  sizeOffsets[j][2] if not isBitField else variableDeclarations[sizeOffsets[j][0]][4]["bitFieldInfo"]["currentBitFieldSequenceContainerSizeInBytes"]
							if sizeOffsets[j][1] < fileDisplayOffset or sizeOffsets[j][1]+numBytesToRead >= min(len(dataBlock),fileDisplayOffset+BLOCK_SIZE): 
								if sizeOffsets[j][1] >= len(dataBlock):	# Even the starting offset itself is bigger than the file size
									notEnoughDataToMap = True
									valueBytes = []
								elif sizeOffsets[j][1]+numBytesToRead >= len(dataBlock):
									notEnoughDataToMap = True
									truncatedSize = len(dataBlock)-sizeOffsets[j][1]
									valueBytes = readBytesFromFile(sizeOffsets[j][1], truncatedSize)
								else:	
									valueBytes = readBytesFromFile(sizeOffsets[j][1], numBytesToRead)
									
								if len(valueBytes) < numBytesToRead and not notEnoughDataToMap:
									OUTPUT("Error in showDataBlock() - len(valueBytes) =",len(valueBytes)," < numBytesToRead (",numBytesToRead,")")
									sys.exit()
									break
							else:
								valueBytes = displayBlock[sizeOffsets[j][1]-fileDisplayOffset : sizeOffsets[j][1]-fileDisplayOffset+numBytesToRead ]
							PRINT ("For variable <", variableName,"> tried to read",numBytesToRead,"bytes from address start", sizeOffsets[j][1]-fileDisplayOffset,"to ", sizeOffsets[j][1]-fileDisplayOffset+numBytesToRead," (excluded), actually read ", len(valueBytes),"bytes")
							if (len(valueBytes) != numBytesToRead) and not notEnoughDataToMap:
								errorMessage = "ERROR: for " + variableName + " tried to read " + STR(numBytesToRead) +" bytes, but succeeded reading only "+STR(len(valueBytes))+" bytes"
								errorRoutine(errorMessage)
								return False
								
							# get the Big endian and Little endian values
							valueBE = ""
							valueLE = ""
							if notEnoughDataToMap:
								pass
							elif datatype in getDictKeyList(structuresAndUnionsDictionary):
								pass
							elif datatype in getDictKeyList(typedefs) and isinstance(typedefs[datatype],list) and len(typedefs[datatype])==2 and (typedefs[datatype][0] == "struct" or typedefs[datatype][0] == "union"):
								pass
							elif isArray and (listItemsProduct(arrayDimensions)>1):
								pass
							elif (len(valueBytes) == 0):
								PRINT ("datatype =%s"%datatype)
								if len(datatype) < len("function") or datatype[:len("function")] != "function":
									errorMessage = "ERROR in showDataBlock(): For variableName =",variableName,"Unknown zero-length non-function datatype = "+ datatype
									errorRoutine(errorMessage)
									return False
							elif (len(valueBytes) in (1,2,4,8)) and (signedOrUnsigned in ("signed","unsigned")):
								if isBitField:
									bitFieldInfo = variableDeclarations[sizeOffsets[j][0]][4]["bitFieldInfo"]
									bitFieldSize = bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"] - bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"] + 1
									bitStartPosition = bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"]
									datatype = bitFieldInfo["currentBitFieldSequenceContainerDatatype"]
								else:
									bitFieldSize = 0
									bitStartPosition = 0
								
								PRINT ("Calling calculateInternalValue for variableName =",variableName,", datatype =",datatype,", bitFieldSize =",bitFieldSize,", bitStartPosition =",bitStartPosition)
								valueBE = calculateInternalValue(valueBytes, BIG_ENDIAN,    datatype, signedOrUnsigned, bitFieldSize, bitStartPosition)
								valueLE = calculateInternalValue(valueBytes, LITTLE_ENDIAN, datatype, signedOrUnsigned, bitFieldSize, bitStartPosition)
							else:
								warningMessage = "WARNING - unhandled case in showDataBlock() for non-array variable <%s> - need to code, len(valueBytes)= %d, current datatype =%s"%(variableName,len(valueBytes),STR(datatype))
								warningRoutine(warningMessage)
							
							valueBEStr = str(valueBE)
							valueLEStr = str(valueLE)
							
							PRINT ("\n"*2,"==="*50,"\ndataLocationOffset =",dataLocationOffset,"File Offset =",fileDisplayOffset,"for variable #",j,"= ",variableDeclarations[sizeOffsets[j][0]][0],"located between address",actualDataAddrStart,"and",actualDataAddrEnd,"valueBytes=0x",valueBytes,"translates into",str(valueLE) + " (LE), " + str(valueBE) + " (BE)" ,"\n","==="*50)
							for i in range(len(valueBytes)): 
								PRINT ("valueBytes[",i,"] = ",ORD(valueBytes[i]) )

							
							
							# Apply the tag to the Hex window
							PRINT ("Going to apply the tag",self.colorTagsData[j],"in Hex window from",startStrHex,"to", endStrHex, "(",startEndStrHex,") for variable",j,variableDeclarations[sizeOffsets[j][0]][0],", with variableDescription =",variableDescription )
							self.viewDataHexText.tag_add(self.colorTagsData[j], startStrHex, endStrHex)
	#						self.viewDataHexText.tag_add(self.colorTagsData[j], startStrHex, startEndStrHex)

							# This is no real list. We just create a fake list so that individual list items (each one is a statement) gets executed.
							# This is a dirty hack, but I don't know how to do it the pythonic way to make multi-statement Lambda functions.
							self.viewDataHexText.tag_bind(self.colorTagsData[j], "<Enter>", 
								lambda event, textValue=variableDescription, addrValueStart=actualDataAddrStart, addrValueEnd=actualDataAddrEnd, 
								lengthValue=dataLengthValue, dataValueLEValue=valueLEStr, dataValueBEValue=valueBEStr, 
								codeVarStart=strCodeWindowVariableStart, codeVarEnd=strCodeWindowVariableEnd : 
								[self.CodeDataMeaningText.configure(text=textValue), 
								 self.dataAddressStartText.configure(text=addrValueStart),
								 self.dataAddressEndText.configure(text=addrValueEnd),
								 self.dataLengthText.configure(text=lengthValue),
								 self.dataValueLEText.configure(text=dataValueLEValue),
								 self.dataValueBEText.configure(text=dataValueBEValue),
								 self.interpretedCodeText.tag_add("yellowbg", codeVarStart, codeVarEnd)])

								 
							self.viewDataHexText.tag_bind(self.colorTagsData[j], "<Leave>", 
								lambda event, textValue="", codeVarStart=strCodeWindowVariableStart, codeVarEnd=strCodeWindowVariableEnd: 
								[self.CodeDataMeaningText.configure(text=textValue), 
								 self.dataAddressStartText.configure(text=""), 
								 self.dataAddressEndText.configure(text=""), 
								 self.dataLengthText.configure(text=""), 
								 self.dataValueLEText.configure(text=""),
								 self.dataValueBEText.configure(text=""),
								 self.interpretedCodeText.tag_remove("yellowbg", codeVarStart, codeVarEnd)])


							# Apply the tag to the ASCII window
							self.viewDataAsciiText.tag_add(self.colorTagsData[j], startStrAscii, endStrAscii)
	#						self.viewDataAsciiText.tag_add(self.colorTagsData[j], startStrAscii, startEndStrAscii)
							self.viewDataAsciiText.tag_bind(self.colorTagsData[j], "<Enter>", 
								lambda event, textValue=variableDescription, addrValueStart=actualDataAddrStart, addrValueEnd=actualDataAddrEnd, 
								lengthValue=dataLengthValue, dataValueLEValue=valueLEStr, dataValueBEValue=valueBEStr, 
								codeVarStart=strCodeWindowVariableStart, codeVarEnd=strCodeWindowVariableEnd: 
								[self.CodeDataMeaningText.configure(text=textValue),
								 self.dataAddressStartText.configure(text=addrValueStart),
								 self.dataAddressEndText.configure(text=addrValueEnd),
								 self.dataLengthText.configure(text=lengthValue),
								 self.dataValueLEText.configure(text=dataValueLEValue),
								 self.dataValueBEText.configure(text=dataValueBEValue),
								 self.interpretedCodeText.tag_add("yellowbg", codeVarStart, codeVarEnd)])
								 
							self.viewDataAsciiText.tag_bind(self.colorTagsData[j], "<Leave>", 
								lambda event, textValue="", codeVarStart=strCodeWindowVariableStart, codeVarEnd=strCodeWindowVariableEnd: 
								[self.CodeDataMeaningText.configure(text=textValue),
								 self.dataAddressStartText.configure(text=""), 
								 self.dataAddressEndText.configure(text=""), 
								 self.dataLengthText.configure(text=""), 
								 self.dataValueLEText.configure(text=""),
								 self.dataValueBEText.configure(text=""),
								 self.interpretedCodeText.tag_remove("yellowbg", codeVarStart, codeVarEnd)])
						
							tags = (self.colorTagsData[tagIndex],)
						
				except IndexError:
					dumpDetailsForDebug()
					errorMessage = "ERROR: Value of index "+ STR(j)+" is out of range - len(sizeOffsets) = "+STR(len(sizeOffsets))
					errorRoutine(errorMessage)
					return False
			if tagIndex == -1:
				dumpDetailsForDebug()
				errorMessage = "ERROR inside showDataBlock() - Invalid tag, exiting"
				errorRoutine(errorMessage)
				return False
			else:
				PRINT ("We already put the tags" )
#				tags = (self.colorTagsData[tagIndex],)
		

		PRINT("Exiting showDataBlock()\n")
		
		return True

	####################################################################
	# This funcion fills one row of the Hex and ASCII windows
	####################################################################
	
	def showIndividualLine(self, row, fileOffset):
		for i in range(len(row)):
			tags = ()
			byte = row[i] 
			byteFileOffset = fileOffset + i
			
			if sizeOffsets and (dataLocationOffset <= byteFileOffset < dataLocationOffset+totalBytesToReadFromDataFile):	# This is data to be colored differently
				tagIndex = -1 		# Default Error value
				for j in range(len(sizeOffsets)):
					if sizeOffsets[j][1] <= byteFileOffset < sizeOffsets[j][1]+sizeOffsets[j][2]:	# This is data to be colored differently
						tagIndex = j	# In case multiple tags match, only the latest (smallest sized) will win by overwriting others
				if tagIndex == -1 and COMPILER_PADDING_ON == False:	# The only way we get a non-coloring within a colored window is when we add compiler paddings
					for item in sizeOffsets:	
						OUTPUT(variableDeclarations[item[0]][0],"<",item[1],",",item[1]+item[2],"> (length", item[2],") <start (inclusive), end (not inclusive)>")
					OUTPUT("dataLocationOffset =",dataLocationOffset, ", fileOffset =",fileOffset,", i =",i,", byteFileOffset =",byteFileOffset, ", totalBytesToReadFromDataFile =",totalBytesToReadFromDataFile,", dataLocationOffset+totalBytesToReadFromDataFile =",dataLocationOffset+totalBytesToReadFromDataFile)
					OUTPUT("\nsizeOffsets =",sizeOffsets,"\n")
					errorMessage = "ERROR in showIndividualLine() for char # %d in current row (overall %d-th byte of file) - Invalid tag, exiting"%(i,byteFileOffset)
					errorRoutine(errorMessage)
					return False
				else:
					try:
						tags = (self.colorTagsData[tagIndex],)
					except IndexError:
						errorMessage = "Inside showIndividualLine(), byte = <"+STR(byte)+"> is causing IndexError for tagIndex = "+STR(tagIndex)+" currently self.colorTagsData= "+STR(self.colorTagsData)
						errorRoutine(errorMessage)
						dumpDetailsForDebug()

			if ((0x20 <= ORD(byte) <= 0x7E) or (0x80 <= ORD(byte) <= 0xFE)):
				byteToPrint = byte
			else:
				byteToPrint = "."
			try:
				tags = ()
				self.viewDataHexText.insert("end", "{:02X}".format(ORD(byte)), tags)
				self.viewDataAsciiText.insert("end", chr(ORD(byteToPrint)), tags)
			except ValueError:
				PRINT ("byte=<",byte,"> is causing ValueError" )
			self.viewDataHexText.insert("end", " ")

		if len(row) < DISPLAY_BLOCK_WIDTH:
			self.viewDataHexText.insert("end", " " * (DISPLAY_BLOCK_WIDTH - len(row)) * 3)
		
		return True

	def openCodeFileDialogue(self, *args):
		global codeFileName
		codeFileName = filedialog.askopenfilename(title="Open - {}".format(TOOL_NAME))
		self.openCodeFile()
		
	def openCodeFile(self, *args):
		if IN_DEMO == True and (codeFileName == None or codeFileName == ""):
			singleCodeLine = ''.join(demoCode)
			PRINT ("singleCodeLine =",singleCodeLine )
			S = tk.StringVar()
			S.set(singleCodeLine)
			PRINT ("StringVar S = <",S.get(),">" )
			self.originalCodeText.delete("1.0", "end")
			self.originalCodeText.insert("end",S.get())
			return True
		
		elif codeFileName != None and codeFileName != "":
			if codeFileName and os.path.exists(codeFileName):
				self.originalCodeText.delete("1.0", "end")
				with open(codeFileName, "r") as codeFile:
					try:
						codeLines = codeFile.readlines()
					except ValueError: # Empty file
						return False
				PRINT ("Code file contains:", codeLines )
				
				singleCodeLine = ''.join(codeLines)
				PRINT ("singleCodeLine =",singleCodeLine )
				S = tk.StringVar()
				S.set(singleCodeLine)
				PRINT ("StringVar S = <",S.get(),">" )
				self.originalCodeText.delete("1.0", "end")
				self.originalCodeText.insert("end",S.get())
				return True
			else:
				errorMessage = "ERROR- Unknown code file name "+codeFileName
				errorRoutine(errorMessage)
				return False

			
	def openDataFileDialogue(self, *args):
		global dataFileName
		'''
		self.viewDataHexText.delete("1.0", "end")
		self.viewDataAsciiText.delete("1.0", "end")
		self.fileOffset.set(0)
		'''
		dataFileNameChosen = filedialog.askopenfilename(title="Open - {}".format(TOOL_NAME))
		
		if dataFileNameChosen == None or dataFileNameChosen == "":
				return
			
		dataFileName = dataFileNameChosen
			
		if fileDisplayOffset != 0:
			self.fileOffset.set(0)
		
		self.openDataFile(dataFileName)

	def openDataFile(self, dataFileNameInput):
		global dataBlock, displayBlock
		
		self.viewDataHexText.delete("1.0", "end")
		self.viewDataAsciiText.delete("1.0", "end")
		
		if openDataFileRoutineBatch(dataFileNameInput) == True:
			size = (dataFileSizeInBytes - BLOCK_SIZE if dataFileSizeInBytes > BLOCK_SIZE else dataFileSizeInBytes - DISPLAY_BLOCK_WIDTH)
			self.parent.title("%s - %s"%(dataFileName, TOOL_NAME))
			self.fileOffsetSpinbox.config(to=max(size, 0))
	
			# MannaManna - BEGIN
			# If the code is already there, and we are just changing the data file, update the data and display block
			if sizeOffsets:
				dataBlock = readBytesFromFile(dataLocationOffset, totalBytesToReadFromDataFile)
				displayBlock = readBytesFromFile(fileDisplayOffset, BLOCK_SIZE)
			# MannaManna - END
			
			
			self.showDataBlock()
			if inputIsHexChar:
				warningMessage = "It appears that the input file is not a binary but rather a text file containing Hex representation of of binary data. Treating it accordingly."
				warningRoutine(warningMessage)
			
			self.dataOffsetEntry.config(state=tk.NORMAL)
			self.fileOffsetEntry.config(state=tk.NORMAL)
			
			return True
		else:
			return False

	def quit(self, event=None):
		self.parent.destroy()
		
	def removeColorTags(self, event=None):
		PRINT ("Removing any existing color tags (if any)...." )
		
		PRINT("Before removing, self.colorTagsCode =",self.colorTagsCode)
		for i in range(len(self.colorTagsCode)):
			self.interpretedCodeText.tag_delete("tag"+str(i))
		self.colorTagsCode = []
		PRINT("After removing, self.colorTagsCode =",self.colorTagsCode)
		
		PRINT("Before removing, self.colorTagsData =",self.colorTagsData)
		for i in range(len(self.colorTagsData)):
			if isinstance(self.colorTagsData[i],list):
				for position in range(len(self.colorTagsData[i])):
					self.viewDataHexText.tag_delete("tag"+str(i)+"_"+str(position))
					self.viewDataAsciiText.tag_delete("tag"+str(i)+"_"+str(position))
			else:
				self.viewDataHexText.tag_delete("tag"+str(i))
				self.viewDataAsciiText.tag_delete("tag"+str(i))
		self.colorTagsData = []
		PRINT("After removing, self.colorTagsData =",self.colorTagsData)

	def clearTreeView(self, event=None):
		
		PRINT ("Currently self.treeView.get_children() = ",self.treeView.get_children(), "len(self.treeView.get_children()) = ",len(self.treeView.get_children()))
		if len(self.treeView.get_children()) > 0:
			PRINT ("Deleting self.treeView.get_children()")
			try:
				currentChildren = self.treeView.get_children()
				for child in currentChildren:
					PRINT ("Just before deleting",child,", self.treeView.get_children() = ",self.treeView.get_children(), "len(self.treeView.get_children()) = ",len(self.treeView.get_children()))
					self.treeView.delete(child)
					PRINT ("Just after deleting",child,", self.treeView.get_children() = ",self.treeView.get_children(), "len(self.treeView.get_children()) = ",len(self.treeView.get_children()))
			except tk.TclError as e:
				sys.stderr.write(str(e)+"\n")
				errorMessage = "Tcl/Tk ERROR while trying to delete existing Tree children"
				errorRoutine(errorMessage)
				return False
			except:
				errorMessage = "Non-Tcl/Tk ERROR while trying to delete existing Tree children"
				errorRoutine(errorMessage)
				return False
				
			PRINT ("After deleting,  self.treeView.get_children() = ",self.treeView.get_children())
		return True

	
	##############################################################################################
	# This function should get called every time the data offset changes, but not the file offset
	##############################################################################################

	def populateDataMap(self, event=None):
		
		PRINT("\n\n\n","==="*50,"\nInside populateDataMap()\n","==="*50)
		
		if lines==[]:
			return True
			
		
#		treeChildrenList = self.treeView.get_children()
#		for treeItem in treeChildrenList:
#			self.treeView.delete(treeItem)
#		selected_item = self.treeView.selection()[0] ## get selected item
#		self.treeView.delete(selected_item)
		self.clearTreeView()

		populateUnraveled()
		
		PRINT ("Inside populateDataMap(), going to write the Root node")
		# The parameter in an insert statement are (parent, index, iid=None, **kw)	
		# Creates a new item and returns the item identifier of the newly created item.
		# parent is the item ID of the parent item, or the empty string to create a new top-level item. 
		# index is an integer, or the value "end", specifying where in the list of parent's children to insert the new item. 
		#     If index is less than or equal to zero, the new node is inserted at the beginning.
		#     If index is greater than or equal to the current number of children, it is inserted at the end. 
		# iid is the item identifier. If iid is specified, iid must not already exist in the tree. Otherwise, a new unique identifier is generated.
		
		PRINT("\n","=="*50,"\n","unraveled (",len(unraveled),"items) =")
		printUnraveled()
		PRINT("\n","=="*50,"\n","Now going to populate the treeview")
		
		currentLevel = 0
		hierarchy = [""]	# The last item indicates what is the current parent
		for N in range(len(unraveled)):
			PRINT ("Before adding, self.treeView.get_children() =",self.treeView.get_children())
			PRINT ("Inserting following node into the treeView:",unraveled[N])
			if N==0 or unraveled[N][0] == unraveled[N-1][0]:	# Do not change the hierarchy
				pass
			elif unraveled[N][0] == unraveled[N-1][0] + 1:		# Add the last node to the hierarchy
				hierarchy.append(id)
			elif unraveled[N][0] < unraveled[N-1][0]:			# Delete the required number of parents until we have a common parent
				levelsToPopFromHierarchy = unraveled[N-1][0] - unraveled[N][0]
				del hierarchy[-levelsToPopFromHierarchy:]
			elif unraveled[N][0] > unraveled[N-1][0] + 1 :		# Should not happen
				errorMessage = "unraveled["+STR(N)+"][0] =",STR(unraveled[N][0]),"cannot be greater than unraveled[",STR(N),"-1][0]+1, which is ",STR(unraveled[N-1][0]+1)
				errorRoutine(errorMessage)
				return False
			levelIndent = "    " * unraveled[N][0]
			dataTypeText = unraveled[N][2] if not isinstance(unraveled[N][2],dict) else unraveled[N][2]["datatype"] if unraveled[N][2]["signedOrUnsigned"] != "unsigned" or unraveled[N][2]["datatype"] == "pointer" else unraveled[N][2]["signedOrUnsigned"] + " " + unraveled[N][2]["datatype"]
			if N<len(unraveled)-1 and unraveled[N][0]==unraveled[N+1][0]-1 and isinstance(unraveled[N][2],dict) and unraveled[N][2]["isArray"]:	# The current node is a parent - an array 
				dataTypeText += " array"
			if isinstance(unraveled[N][2],dict) and unraveled[N][2]["datatype"].startswith("function "):	# Hardcode it for functions
				dataTypeText = "function"
			try:
				if isinstance(unraveled[N][2],dict) and "isBitField" in getDictKeyList(unraveled[N][2]) and unraveled[N][2]["isBitField"]==True:
					addrStart = hex(unraveled[N][3]+integerDivision(unraveled[N][2]["bitFieldInfo"]["currentBitFieldSequenceCurrentContainerBitIndexStart"],BITS_IN_BYTE)) + "." + STR(unraveled[N][2]["bitFieldInfo"]["currentBitFieldSequenceCurrentContainerBitIndexStart"]%BITS_IN_BYTE)
					addrEnd = hex(unraveled[N][3]+integerDivision(unraveled[N][2]["bitFieldInfo"]["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"],BITS_IN_BYTE)) + "." + STR(unraveled[N][2]["bitFieldInfo"]["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"]%BITS_IN_BYTE)
				else:
					addrStart = hex(unraveled[N][3])
					addrEnd = hex(unraveled[N][4]-1)
#				treeViewRowValues = (levelIndent+unraveled[N][1],dataTypeText,hex(unraveled[N][3]),hex(unraveled[N][4]-1),unraveled[N][5],unraveled[N][6],unraveled[N][7])
				treeViewRowValues = (levelIndent+unraveled[N][1],dataTypeText,addrStart,addrEnd,unraveled[N][5],unraveled[N][6],unraveled[N][7])
				id = self.treeView.insert(hierarchy[-1], "end", iid=None, values=treeViewRowValues)
			except IndexError:
				OUTPUT ("IndexError in populateDataMap(): List index out of range for N = ",N)
				OUTPUT (unraveled[N])
				sys.exit()
			PRINT ("After adding, self.treeView.get_children() =",self.treeView.get_children())
		
		# Print it on the console and the CSV file
#		self.prettyPrintUnraveled()
		prettyPrintUnraveled()
		return True
			
	############################################################################################################################
	############################################################################################################################
	#
	# interpret
	#
	############################################################################################################################
	############################################################################################################################

	def interpret(self, event=None):
		global lines
		
		PRINT("\n\n\n","==="*50,"\nInside interpret()\n","==="*50)
		
#		self.parent.config(cursor="wait")		# MannaManna
		inputCodeContents = self.originalCodeText.get("1.0", "end")
		PRINT ("type(inputCodeContents) =", type(inputCodeContents) )	#Python 2 will have the type as unicode, Python 3 as bytes
		
		if PYTHON2x:
			inputCodeContents = inputCodeContents.encode("ascii","ignore")
		PRINT ("type(inputCodeContents) =", type(inputCodeContents) )	#Python 2 will have the type as unicode, Python 3 as bytes

		inputCodeContents = convert2Str(inputCodeContents)
		PRINT ("After convert2Str(inputCodeContents), type(inputCodeContents) =", type(inputCodeContents) )	#Now everything should be str

		
		# Verify that the inputCodeContents is indeed string
		if not checkIfString(inputCodeContents):
			errorMessage = "ERROR in coding: inputCodeContents is NOT string - type(inputCodeContents) = "+STR(type(inputCodeContents))
			errorRoutine(errorMessage)
			return False
		
		asciiLines = inputCodeContents.splitlines()
		if not checkIfStringOrListOfStrings(asciiLines):
			errorMessage = "ERROR in coding: asciiLines is NOT string - type(asciiLines) = "+STR(type(asciiLines))
			errorRoutine(errorMessage)
			return False
		
#		asciiLines = self.originalCodeText.get('1.0', 'end-1c').splitlines()
		PRINT ("Content of input code box =" )
		PRINT (inputCodeContents )
		PRINT ("asciiLines =",asciiLines )
		PRINT ("type(asciiLines) =",type(asciiLines) )
		# We need to check what is the type of individual lines of asciiLines
		PRINT ("type(asciiLines[0]) =",type(asciiLines[0]) )
#		sys.exit()
		
		# Empty the global variables
		self.removeColorTags()
		self.clearTreeView()
		
		# Empty the global variables
		lines=[]
		for line in asciiLines:
			lines.append(line+'\n')

		interpretBatchResult = interpretBatch()

		# Call the main module
		if interpretBatchResult == False:
			OUTPUT ("ERROR in interpret() after calling mainWork() - exiting" )
			self.parent.config(cursor="")		# MannaManna
			return False

		# Only after the interpretation goes through, enable the Interpreted code window
		self.interpretedCodeText.config(state=tk.NORMAL)
			
		PRINT ("lines =", lines )
		singleLine = ''.join(lines)
		PRINT ("singleLine =",singleLine )
		S = tk.StringVar()
		S.set(singleLine)
		PRINT ("StringVar S = <",S.get(),">" )
		self.interpretedCodeText.delete("1.0", "end")
		
		#self.interpretedCodeText.insert("end",inputCodeContents)
		self.interpretedCodeText.insert("end",S.get())
		
		# Now we are going to add code that will highlight the variable declarations with a suitable descriptions
		
		PRINT ("inside interpret(), tokenLocationLinesChars = ",tokenLocationLinesChars )
		for item in variableDeclarations:
			PRINT ("Variable declared is ...." )
			PRINT (item )
			try:
				variableDescription = item[4]["description"]
				variableTokenIndex = item[4]["globalTokenListIndex"]	# This is the ABOSLUTE index of the variable name token inside the whole tokenlist. 
												# Recall the item[3] is the relative index of the variable name within the variable declaration statement.
												# For cases where the statement does not exist inside the actual code file (like the builtin typedefs)
				if variableTokenIndex >= 0:
					variableLocationStart = tokenLocationLinesChars[variableTokenIndex][0]
					variableLocationEnd   = tokenLocationLinesChars[variableTokenIndex][1]
					PRINT ("variable", item[0],"starts from", variableLocationStart, "and ends at", variableLocationEnd )
					variableLocationStartStr = ""+ str(variableLocationStart[0]+1)+"."+str(variableLocationStart[1])	# Recall that on Text widget the line # starts from 1, not 0
					variableLocationEndStr   = ""+ str(variableLocationEnd[0]  +1)+"."+str(variableLocationEnd[1])	# Recall that on Text widget the line # starts from 1, not 0
					PRINT ("variable", item[0],"starts from", variableLocationStartStr, "and ends at", variableLocationEndStr )
					'''
					tagName = "tag" + str(variableTokenIndex)
					self.interpretedCodeText.tag_add(tagName,variableLocationStartStr,variableLocationEndStr)
					self.interpretedCodeText.tag_configure(tagName, background="white", foreground="black")
					self.interpretedCodeText.tag_bind(tagName, "<Enter>", lambda event, textValue=variableDescription : 
								self.CodeDataMeaningText.configure(text=textValue))	
					self.interpretedCodeText.tag_bind(tagName, "<Leave>", lambda event, textValue="" : self.CodeDataMeaningText.configure(text=textValue))
					'''
			except IndexError:
				OUTPUT("Current item =",item)
				OUTPUT("variableTokenIndex =",variableTokenIndex)
				OUTPUT("tokenLocationLinesChars[variableTokenIndex=%d]=%s"%(variableTokenIndex,STR(tokenLocationLinesChars[variableTokenIndex])))
				sys.exit()
#		self.parent.config(cursor="")		# MannaManna
		return True

	##################################################################################################################
	#
	# The only purpose of this function is so see which all variables get selected.
	#
	##################################################################################################################
	
	def mapStructureToData(self, event=None):
		global variableSelectedIndices

		PRINT("\n\n\n","==="*50,"\nInside mapStructureToData()\n","==="*50)
		
		if lines==[]:
			return False
		elif not dataFileName:
			errorMessage = "Cannot map structure without data"
			errorRoutine(errorMessage)
			return False
		
		for treeItem in self.treeView.get_children():
			self.treeView.delete(treeItem)
		
		try:
			selectionRanges = self.interpretedCodeText.tag_ranges(tk.SEL)
		except UnboundLocalError:
			PRINT ("ERROR in mapStructureToData() - no selection made - exiting" )
			return False
			sys.exit()
			
		if selectionRanges:	
			PRINT ("selectionRanges =",selectionRanges )
			PRINT ("tk.SEL_FIRST =",selectionRanges[0], "tk.SEL_LAST =",selectionRanges[1] )
			selectionRangeStart = "%s"%(selectionRanges[0])
			selectionRangeEnd = "%s"%(selectionRanges[1])
		else:
			PRINT ('NO Selected Text - assuming whole window is selected')
			selectionRangeStart = "1.0"
			selectionRangeEnd = str(len(lines))+"."+str(len(lines[-1])-1)

		selectionRangeStartLineNum = int(selectionRangeStart.split(".")[0])-1	# Remember that in Text widget the line # starts from 1, not 0
		selectionRangeStartCharNum = int(selectionRangeStart.split(".")[1])
		selectionRangeEndLineNum = int(selectionRangeEnd.split(".")[0])-1		# Remember that in Text widget the line # starts from 1, not 0
		selectionRangeEndCharNum = int(selectionRangeEnd.split(".")[1])
		PRINT ("selectionRangeStart =",selectionRangeStart,"<",selectionRangeStartLineNum,".", selectionRangeStartCharNum,">","type(selectionRangeStart) =",type(selectionRangeStart), "selectionRangeEnd =",selectionRangeEnd,"<",selectionRangeEndLineNum,".", selectionRangeEndCharNum,">","type(selectionRangeEnd) =",type(selectionRangeEnd) )
		PRINT ('SELECTED Text is %r' % self.interpretedCodeText.get(selectionRangeStart, selectionRangeEnd))
		
		PRINT ("Inside mapStructureToData(), tokenLocationLinesChars =",tokenLocationLinesChars )
		tokenListResult = tokenizeLines(lines)
		if tokenListResult == False:
			PRINT ("ERROR inside mapStructureToData after calling tokenizeLines(lines) for lines = ", lines )
			return False
		else:
			tokenList = tokenListResult[0]
			
		if len(tokenList) != len(tokenLocationLinesChars):
			errorMessage = "ERROR in mapStructureToData() - somehow we have mismatching tokenList and tokenLocationLinesChars - exiting" 
			errorRoutine(errorMessage)
			return False
			
		# Find index of the first token selected
		selectionStartIndex = -100000
		i = 0
		for i in range(len(tokenLocationLinesChars)):
			if (selectionRangeStartLineNum < tokenLocationLinesChars[i][0][0]) or ((selectionRangeStartLineNum == tokenLocationLinesChars[i][0][0]) and (selectionRangeStartCharNum < tokenLocationLinesChars[i][0][1])):
				selectionStartIndex = i
				break
			elif ((tokenLocationLinesChars[i][0][0] <= selectionRangeStartLineNum <= tokenLocationLinesChars[i][1][0]) and
				  (tokenLocationLinesChars[i][0][1] <= selectionRangeStartCharNum <= tokenLocationLinesChars[i][1][1])):
				selectionStartIndex = i
				break
				
		# Find index of the last token selected (this is the index of just tokens, not necessarily variable. Then we will compare it with the globalTokenListIndex for each variable
		selectionEndIndex = -100000
		i = len(tokenLocationLinesChars)-1
		while i >= 0:
			if (selectionRangeEndLineNum > tokenLocationLinesChars[i][1][0]) or ((selectionRangeEndLineNum == tokenLocationLinesChars[i][1][0]) and (selectionRangeEndCharNum > tokenLocationLinesChars[i][1][1])):
				selectionEndIndex = i
				break
			elif ((tokenLocationLinesChars[i][0][0] <= selectionRangeEndLineNum <= tokenLocationLinesChars[i][1][0]) and
				  (tokenLocationLinesChars[i][0][1] <= selectionRangeEndCharNum <= tokenLocationLinesChars[i][1][1])):
				selectionEndIndex = i
				break
			i = i - 1

		variableSelectedIndices = []
		if (0 <= selectionStartIndex < len(tokenLocationLinesChars)) and (0 <= selectionEndIndex < len(tokenLocationLinesChars)):
			k = 0
			while k in range(len(variableDeclarations)):
				item = variableDeclarations[k]
				if variableDeclarations[k][4]["variableId"] != k:
					errorMessage = "ERROR - wrong value of variableId - exiting"
					errorRoutine(errorMessage)
					return False
				elif (selectionStartIndex <= item[4]["globalTokenListIndex"] <= selectionEndIndex):
					variableSelectedIndices.append(item[4]["variableId"])
				k += 1
		PRINT("variableSelectedIndices =",variableSelectedIndices)
		PRINT("globalScopes[variableId, scopeStartVariableId, scopeEndVariableId] =",globalScopes)
		dumpDetailsForDebug()
		
		self.selectVariablesAtGlobalScope()
		self.calculateSizeOffsets()
		self.performInterpretedCodeColoring()
		self.populateDataMap()
		
	#####################################################################################################################################
	#                                                                                                                        			#
	#	Calculate the sizeOffsets and totalBytesToReadFromDataFile based on the variablesAtGlobalScopeSelected and dataLocationOffset   #
	#                                                                                                                        			#
	#####################################################################################################################################
		
	def selectVariablesAtGlobalScope(self, event=None):
		global variablesAtGlobalScopeSelected, globalScopesSelected
		
		# globalScopes - the global variables that have level=0, including the typedefs. Its format is [variableId, scopeStartVariableId, scopeEndVariableId]
		# globalScopesSelected - A subset of the globalScopes, excluding the builtin typedefs, and rest of the typedefs too depending on the value of the MAP_TYPEDEFS_TOO
		# variablesAtGlobalScopeSelected - A subset of globalScopesSelected, depending on the user selection (captured by variableSelectedIndices)
		
		globalScopesSelected = []
		PRINT ("Original globalScopes = ", globalScopes)
		for i in range(len(globalScopes)):
			varIndex = globalScopes[i][0]
			PRINT("i =",i,"variableDeclarations[varIndex] =",variableDeclarations[varIndex])
			if 'typedef' in variableDeclarations[varIndex][2]: 
				if MAP_TYPEDEFS_TOO:
					PRINT("Counting typedefs")
					# We can never select builtin typedefs since there is no code to color
					if variableDeclarations[varIndex][4]["globalTokenListIndex"] >= 0:
						globalScopesSelected.append(globalScopes[i])
				else:	
					PRINT("Cannot count typedefs")
				pass
			else:
				PRINT("Counting non-typedef")
				globalScopesSelected.append(globalScopes[i])
				
		PRINT ("globalScopes = ", globalScopes)
		PRINT ("Modified globalScopesSelected = ", globalScopesSelected)
		
		# We want to find out which all variable ids in a contiguous area will be included. Basically, if you select ANY variable under a global-scope-variable,
		# ALL the variables under that global scope get selected.
		
		variablesAtGlobalScopeSelected = []
		# Now check which all variables at the Global scope should be colored
		# Remember that globalScopes list of the format [variableId, scopeStartVariableId, scopeEndVariableId]
		# So, the chosen varIndex must match either the global variable iteself, or must lie within its scope
		for varIndex in variableSelectedIndices:
			for item in globalScopesSelected:
				if varIndex == item[0] or (item[1] <= varIndex <= item[2]):
					if item[0] not in variablesAtGlobalScopeSelected:
						variablesAtGlobalScopeSelected.append(item[0])
		PRINT("variablesAtGlobalScopeSelected =",variablesAtGlobalScopeSelected)
		
		if not variablesAtGlobalScopeSelected:
			dumpDetailsForDebug(True)
		
	#####################################################################################################################################
	#                                                                                                                        			#
	#	Calculate the sizeOffsets and totalBytesToReadFromDataFile based on the variablesAtGlobalScopeSelected and dataLocationOffset   #
	#                                                                                                                        			#
	#####################################################################################################################################
		
	def calculateSizeOffsets(self, event=None):
		PRINT("\n\n\n","==="*50,"\nInside calculateSizeOffsets()\n","==="*50)
		self.removeColorTags()
		
		calculateSizeOffsetsBatch()
	
		PRINT ("Going to read totalBytesToReadFromDataFile =", totalBytesToReadFromDataFile,"bytes from file ", dataFileName,"from offset",dataLocationOffset)
#		dataBlock = readBytesFromFile(dataLocationOffset, totalBytesToReadFromDataFile)
		self.updateDataBlock()
		return True
		
	##########################################################################################################################
	#                                                                                                                        #
	#	Color-codes the Interpreted Code window  (it already assumes that sizeOffsets has been re-calculated)                #
	#                                                                                                                        #
	##########################################################################################################################
		
	
	def performInterpretedCodeColoring(self, event=None):

		PRINT ("\n"*3,"==="*50,"\n Inside performInterpretedCodeColoring(), for data Offset =",dataLocationOffset)
		PRINT ("File Offset = self.fileOffset.get() =",self.fileOffset.get(),"\n","=="*50,"\n"*3)
		
		PRINT ("We have the sizeOffsets =",sizeOffsets)
		PRINT ("Recall that sizeOffsets has absolute offsets, not relative to the display window")
		
		if not sizeOffsets:
			return True
		elif len(sizeOffsets) <= 10:
			self.COLORS = COLORS_10
		elif len(sizeOffsets) <= 20:
			self.COLORS = COLORS_20
		else:
			self.COLORS = COLORS_ALL
				
		# Figure out how many different colored tags one would need to create
		PRINT ("Number of color tags to be created = ", len(sizeOffsets) )
		
		# TO-DO: I am not fully sure if this will work below. If it does not, just explicitly clear them (the 2 lines below it)
		self.removeColorTags()
#		self.colorTagsCode = []
#		self.colorTagsData = []
		
		for i in range(len(sizeOffsets)):
		
			variableName = variableDeclarations[sizeOffsets[i][0]][0]
			variableDescription = variableDeclarations[sizeOffsets[i][0]][4]["description"] 
			signedOrUnsigned = variableDeclarations[sizeOffsets[i][0]][4]["signedOrUnsigned"]
			datatype = variableDeclarations[sizeOffsets[i][0]][4]["datatype"]
			isArray = variableDeclarations[sizeOffsets[i][0]][4]["isArray"]
			arrayDimensions = variableDeclarations[sizeOffsets[i][0]][4]["arrayDimensions"] if isArray else []
			isBitField = variableDeclarations[sizeOffsets[i][0]][4]["isBitField"]
			
			PRINT("Coloring variable",variableName,"with",self.COLORS[i%len(self.COLORS)])
			
			# Handle the Data windows. Remember that if the variable is an array, there will be multiple same-color tags (but with different hovertexts) for the same variable
			if isArray:		# The item is an array
				PRINT ("Creating multiple Data tags for Array item",variableDeclarations[sizeOffsets[i][0]][0] )
				totalNumberOfArrayElements = listItemsProduct(arrayDimensions)
				if totalNumberOfArrayElements == False:
					errorMessage = "ERROR calculating totalNumberOfArrayElements = listItemsProduct(arrayDimensions="+STR(arrayDimensions)+")"
					errorRoutine(errorMessage)
					return False
				else:
					PRINT ("Creating",totalNumberOfArrayElements,"different color tags for array variable",variableName )
					colorTagsForArrayVariable = []
					for position in range(totalNumberOfArrayElements):
						colorTagsForArrayVariable.append("tag"+str(i)+"_"+str(position))
					PRINT ("Before adding tags for array variable", variableName, ", self.colorTagsData =",self.colorTagsData)
					self.colorTagsData.append(colorTagsForArrayVariable)
					PRINT ("After adding tags for array variable", variableName, ", self.colorTagsData =",self.colorTagsData)
					for position in range(totalNumberOfArrayElements):
						self.viewDataHexText.tag_configure  (self.colorTagsData[i][position], foreground=self.COLORS[i%len(self.COLORS)])
						self.viewDataAsciiText.tag_configure(self.colorTagsData[i][position], foreground=self.COLORS[i%len(self.COLORS)])
					PRINT ("\n\n\nCreated",self.colorTagsData[i],"for array variable", variableName, "with foreground=",self.COLORS[i%len(self.COLORS)] )
			else:
				PRINT ("Before adding tags for non-array variable", variableName, ", self.colorTagsData =",self.colorTagsData)
				self.colorTagsData.append("tag"+str(i))
				PRINT ("After adding tags for non-array variable", variableName, ", self.colorTagsData =",self.colorTagsData)
				self.viewDataHexText.tag_configure  (self.colorTagsData[i], foreground=self.COLORS[i%len(self.COLORS)])
				self.viewDataAsciiText.tag_configure(self.colorTagsData[i], foreground=self.COLORS[i%len(self.COLORS)])
				
			
			# For the Interpreted code window, find out the locations of the variable names (to which the tags would apply)
			tokenStartLineNum = tokenLocationLinesChars[variableDeclarations[sizeOffsets[i][0]][4]["globalTokenListIndex"]][0][0]
			tokenStartCharNum = tokenLocationLinesChars[variableDeclarations[sizeOffsets[i][0]][4]["globalTokenListIndex"]][0][1]
			tokenEndLineNum = tokenLocationLinesChars[variableDeclarations[sizeOffsets[i][0]][4]["globalTokenListIndex"]][1][0]
			tokenEndCharNum = tokenLocationLinesChars[variableDeclarations[sizeOffsets[i][0]][4]["globalTokenListIndex"]][1][1]
			strStart = str(tokenStartLineNum+1)+"."+str(tokenStartCharNum)		# Remember that on Text the line number starts from 1, not 0
			strEnd   = str(tokenEndLineNum  +1)+"."+str(tokenEndCharNum+1)		# Remember that on Text the line number starts from 1, not 0
			
			# Create the tag for the Interpreted code window
			PRINT ("Before adding, self.colorTagsCode = ",self.colorTagsCode)
			self.colorTagsCode.append("tag"+str(i))
			self.interpretedCodeText.tag_configure(self.colorTagsCode[i], foreground=self.COLORS[i%len(self.COLORS)])
			PRINT ("\n\n\nCreated",self.colorTagsCode[i],"with foreground=",self.COLORS[i%len(self.COLORS)],"for the Code window" )
			PRINT ("After adding, self.colorTagsCode = ",self.colorTagsCode)
			
			# BEGIN Value added here
			
			# We do NOT get the data from the displayed Hex or Ascii window. We get it from the original File.
			# This the actual file offset the variable starts from (this could actually be before the current frame)
			if isBitField:
				bitFieldInfo = variableDeclarations[sizeOffsets[i][0]][4]["bitFieldInfo"]
				actualDataAddrStart = "0x{:X}".format(sizeOffsets[i][1] + integerDivision( bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"],BITS_IN_BYTE)) +"." + STR(bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"]%BITS_IN_BYTE) + " (LE)"
				# This End byte is INCLUDED
				actualDataAddrEnd   = "0x{:X}".format(sizeOffsets[i][1] + integerDivision( bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"],BITS_IN_BYTE)) +"." + STR(bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"]%BITS_IN_BYTE) + " (LE)"
				dataLengthValue = STR(variableDeclarations[sizeOffsets[i][0]][4]["bitFieldWidth"]) + " bits"
			else:
				actualDataAddrStart = "0x{:010X}".format(sizeOffsets[i][1])
				actualDataAddrEnd   = "0x{:010X}".format(sizeOffsets[i][1]+sizeOffsets[i][2]-1)	# This byte is INCLUDED
				dataLengthValue = STR(sizeOffsets[i][2])+" byte" + ("s" if sizeOffsets[i][2] > 1 else "")
			
			numBytesToRead =  sizeOffsets[i][2] if not isBitField else variableDeclarations[sizeOffsets[i][0]][4]["bitFieldInfo"]["currentBitFieldSequenceContainerSizeInBytes"]
			
			valueBytes = dataBlock[ sizeOffsets[i][1]-dataLocationOffset : sizeOffsets[i][1]+numBytesToRead-dataLocationOffset ]

			PRINT ("\n\n")
			PRINT ("valueBytes = displayBlock[sizeOffsets[",i,"][1]-fileDisplayOffset : sizeOffsets[",i,"][1]-fileDisplayOffset+sizeOffsets[",i,"][2]] ")
			PRINT ("valueBytes = displayBlock[", sizeOffsets[i][1]-fileDisplayOffset, ":", sizeOffsets[i][1]-fileDisplayOffset+sizeOffsets[i][2],"] ")
			PRINT ("Length of valueBytes =",len(valueBytes))

			# get the Big endian and Little endian values
			valueBE = ""
			valueLE = ""
			if len(valueBytes) != numBytesToRead:	# Incomplete data
				pass
			elif datatype in getDictKeyList(structuresAndUnionsDictionary):
				pass
			elif datatype in getDictKeyList(typedefs) and isinstance(typedefs[datatype],list) and len(typedefs[datatype])==2 and (typedefs[datatype][0] == "struct" or typedefs[datatype][0] == "union"):
				pass
			elif isArray and (listItemsProduct(arrayDimensions)>1):
				pass
			elif (len(valueBytes) in (1,2,4,8)) and (signedOrUnsigned in ("signed","unsigned")):
				if isBitField:
					bitFieldInfo = variableDeclarations[sizeOffsets[i][0]][4]["bitFieldInfo"]
					bitFieldSize = bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexEndInclusive"] - bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"] + 1
					bitStartPosition = bitFieldInfo["currentBitFieldSequenceCurrentContainerBitIndexStart"]
					datatype = bitFieldInfo["currentBitFieldSequenceContainerDatatype"]
				else:
					bitFieldSize = 0
					bitStartPosition = 0
						
				valueBE = calculateInternalValue(valueBytes, BIG_ENDIAN,    datatype, signedOrUnsigned, bitFieldSize, bitStartPosition) 
				valueLE = calculateInternalValue(valueBytes, LITTLE_ENDIAN, datatype, signedOrUnsigned, bitFieldSize, bitStartPosition)
			elif len(valueBytes)==0 and datatype.startswith("function "):
				PRINT("Functions do not have a storage")
			else:
				OUTPUT ("\n\nError in performInterpretedCodeColoring() - unhandled case of datatype =",datatype,"and len(valueBytes) =",len(valueBytes),"- need to code\n\n" )
				sys.exit()
				
			valueBEStr = str(valueBE)
			valueLEStr = str(valueLE)
			
			PRINT ("for variable #",i,"= ",variableDeclarations[sizeOffsets[i][0]][0],"valueBytes = datafile[",sizeOffsets[i][1],",",sizeOffsets[i][1]+sizeOffsets[i][2], "] =0x",valueBytes,"translates into",str(valueLE) + " (LE), " + str(valueBE) + " (BE)" )
			for k in range(len(valueBytes)): 
				PRINT ("valueBytes[",k,"] = ",ORD(valueBytes[k]) )
			
			# END Value added here

			# We check if the value corresponding to the variable exists within the current display window (whether the return value from getDataCoordinates() is true or not)
			# If the return value from getDataCoordinates() is False, that means the data corresponding to this variable does not exist within the current display window.

			getDataCoordinatesResult = self.getDataCoordinates( sizeOffsets[i][1], sizeOffsets[i][1]+sizeOffsets[i][2] )
			if getDataCoordinatesResult == False:
				PRINT ("Data for Variable <",variableName,"> located at File[",  sizeOffsets[i][1],":", sizeOffsets[i][1]+sizeOffsets[i][2], "] is NOT displayable within current window.")
				PRINT ("data offset = ",dataLocationOffset,"file offset =",fileDisplayOffset,"Hence just being content with the variable description.")
				PRINT ("Going to apply the tag",self.colorTagsCode[i],"in interpreted code window from",strStart,"to", strEnd, "for variable #",i,variableDeclarations[sizeOffsets[i][0]][0],", with variableDescription =",variableDescription )
				self.interpretedCodeText.tag_add(self.colorTagsCode[i], strStart, strEnd)

				self.interpretedCodeText.tag_bind(self.colorTagsCode[i], "<Enter>", 
					lambda event, textValue=variableDescription, addrValueStart=actualDataAddrStart, addrValueEnd=actualDataAddrEnd, 
					lengthValue=dataLengthValue, dataValueLEValue=valueLEStr, dataValueBEValue=valueBEStr:
					[self.CodeDataMeaningText.configure(text=textValue), 
					 self.dataAddressStartText.configure(text=addrValueStart),
					 self.dataAddressEndText.configure(text=addrValueEnd),
					 self.dataLengthText.configure(text=lengthValue),
					 self.dataValueLEText.configure(text=dataValueLEValue),
					 self.dataValueBEText.configure(text=dataValueBEValue)])

				self.interpretedCodeText.tag_bind(self.colorTagsCode[i], "<Leave>", 
					lambda event:
					[self.CodeDataMeaningText.configure(text=""), 
					 self.dataAddressStartText.configure(text=""), 
					 self.dataAddressEndText.configure(text=""), 
					 self.dataLengthText.configure(text=""), 
					 self.dataValueLEText.configure(text=""),
					 self.dataValueBEText.configure(text="")])

			else:
				printMessage = "For data item # i=<%d>, %s, getDataCoordinates(dataByteStartOffset=%d, dataByteEndOffset=%d) = %s!"%(i, variableDescription, sizeOffsets[i][1], sizeOffsets[i][1]+sizeOffsets[i][2], STR(getDataCoordinatesResult))
				PRINT (printMessage )
				PRINT ("Data for Variable <",variableName,"> located at File[",sizeOffsets[i][1],":", sizeOffsets[i][1]+sizeOffsets[i][2], "] is displayable within current window.")
				PRINT ("data offset = ",dataLocationOffset,"file offset =",fileDisplayOffset,"Hence doing all the coloring stuff")
				
				startStrHex   = getDataCoordinatesResult[0][0]
				endStrHex     = getDataCoordinatesResult[0][1]
				startStrAscii = getDataCoordinatesResult[1][0]
				endStrAscii   = getDataCoordinatesResult[1][1]
				
				
				PRINT ("Going to apply the tag",self.colorTagsData[i],"in Hex window from",startStrHex,"to", endStrHex, "for variable",i,variableDeclarations[sizeOffsets[i][0]][0],", with variableDescription =",variableDescription )
				self.viewDataHexText.tag_add(self.colorTagsData[i], startStrHex, endStrHex)
#				self.viewDataHexText.tag_add(self.colorTagsData[i], startStrHex, startEndStrHex)

				# Did we forget to do this earlier?
				PRINT ("Going to apply the tag",self.colorTagsData[i],"in Ascii window from",startStrAscii,"to", endStrAscii, "for variable",i,variableDeclarations[sizeOffsets[i][0]][0],", with variableDescription =",variableDescription )
				self.viewDataAsciiText.tag_add(self.colorTagsData[i], startStrAscii, endStrAscii)

				PRINT ("Going to apply the tag",self.colorTagsCode[i],"in interpreted code window from",strStart,"to", strEnd, "for variable",i,variableDeclarations[sizeOffsets[i][0]][0],", with variableDescription =",variableDescription )
				self.interpretedCodeText.tag_add(self.colorTagsCode[i], strStart, strEnd)
			

				# This is no real list. We just create a fake list so that individual list items (each one is a statement) gets executed.
				# This is a dirty hack, but I don't know how to do it the pythonic way to make multi-statement Lambda functions.
				self.interpretedCodeText.tag_bind(self.colorTagsCode[i], "<Enter>", 
					lambda event, textValue=variableDescription, addrValueStart=actualDataAddrStart, addrValueEnd=actualDataAddrEnd, 
					lengthValue=dataLengthValue, dataValueLEValue=valueLEStr, dataValueBEValue=valueBEStr, 
					HexVarStart=startStrHex, HexVarEnd=endStrHex, AsciiVarStart=startStrAscii, AsciiVarEnd=endStrAscii :
					[self.CodeDataMeaningText.configure(text=textValue), 
					 self.dataAddressStartText.configure(text=addrValueStart),
					 self.dataAddressEndText.configure(text=addrValueEnd),
					 self.dataLengthText.configure(text=lengthValue),
					 self.dataValueLEText.configure(text=dataValueLEValue),
					 self.dataValueBEText.configure(text=dataValueBEValue),
					 self.viewDataHexText.tag_add("yellowbg", HexVarStart, HexVarEnd),
					 self.viewDataAsciiText.tag_add("yellowbg", AsciiVarStart, AsciiVarEnd)])

					 
				self.interpretedCodeText.tag_bind(self.colorTagsCode[i], "<Leave>", 
					lambda event, HexVarStart=startStrHex, HexVarEnd=endStrHex, AsciiVarStart=startStrAscii, AsciiVarEnd=endStrAscii :
					[self.CodeDataMeaningText.configure(text=""), 
					 self.dataAddressStartText.configure(text=""), 
					 self.dataAddressEndText.configure(text=""), 
					 self.dataLengthText.configure(text=""), 
					 self.dataValueLEText.configure(text=""),
					 self.dataValueBEText.configure(text=""),
					 self.viewDataHexText.tag_remove("yellowbg", HexVarStart, HexVarEnd),
					 self.viewDataAsciiText.tag_remove("yellowbg", AsciiVarStart, AsciiVarEnd)])
			
		# After all the tags have been created, do some sanity checks.
		if len(self.colorTagsCode) != len(sizeOffsets) or len(sizeOffsets) != len(self.colorTagsData):
			dumpDetailsForDebug()
			errorMessage("Mismatching size of self.colorTagsCode, self.colorTagsData and sizeOffsets")
			errorRoutine(errorMessage)
			return False
			
		if dataFileName:
			PRINT ("Re-displaying the data displayBlock" )
			self.showDataBlock()

		return True

		
	##########################################################################################################################
	#                                                                                                                        #
	#	Run a Demo                                                                                                           #
	#                                                                                                                        #
	##########################################################################################################################
	def runDemo(self, event=None):
		global IN_DEMO
		IN_DEMO = True
		warningMessage = "First we are going to use an arbitrary file as the datastream to be parsed. We choose this script itself as data. Press OK to continue."
		warningRoutine(warningMessage)
		dataFileNameInput = sys.argv[0]
		PRINT("dataFileNameInput is set to <",sys.argv[0],">")
		self.openDataFile(dataFileNameInput)
		warningMessage = "Next we are going to use some code as the input format of the datastream to be parsed. Press OK to continue."
		warningRoutine(warningMessage)
		self.openCodeFile("junk")
		warningMessage = "Now that you can see the code on the left and the data on the right, we are going to interpret the code. Press OK to continue."
		warningRoutine(warningMessage)
		self.interpret()
		warningMessage = "Now that you can see the interpreted code in the middle window, we are going to map the interpreted code to the data. Press OK to continue."
		warningRoutine(warningMessage)
		self.mapStructureToData()
		warningMessage = "We map the data format from the offset of 0 by default. Of course, we can change that. Let's see what happens when we map it from one-fourth of a Kilobyte. You can specify this in any format, as pure 256, or 0x100, or even 1KB/4, which is very much human readable. Press OK to continue."
		warningRoutine(warningMessage)
		self.dataOffsetEntry.insert(tk.END,"1KB/4")
		self.dataOffset.set(256)
		self.mapStructureToData()
		warningMessage = "Now you see, that data mapping is happening from the offset of 0x100. Press OK to continue."
		warningRoutine(warningMessage)
		warningMessage = "We selected ALL the gloabal-level variables for mapping. But, during regular run (not in Demo) you could also select any Interpreted code segment using your mouse and click on the Map button, and all the top-level global variables within that selection will get mapped. Press OK to continue."
		warningRoutine(warningMessage)
#		self.interpretedCodeText.see("1000.0")
#		self.interpretedCodeText.see("65.0")
		warningMessage = "Once all these warning windows go away, take your cursor above various colored items in the interpreted code window and the data window and see how the Description, Address and Values are shown below. \nAlso, play with the Expand/Collapse buttons to see the internals of the mapped variables.\nTo end this Demo, press the \"Clear Demo\" button. Press OK to continue."
		warningRoutine(warningMessage)

	############################################################################################################################
	############################################################################################################################
	#
	# clearDemo
	#
	############################################################################################################################
	############################################################################################################################

	def clearDemo(self, event=None):
		global codeFileName, lines, dataFileName, dataBlock, displayBlock
		global lines, tokenLocationLinesChars, enums, enumFieldValues, typedefs, structuresAndUnionsDictionary, unraveled
		global dummyVariableCount, totalVariableCount, globalScopes, sizeOffsets, variablesAtGlobalScopeSelected
		global pragmaPackCurrentValue, pragmaPackStack

		PRINT ("\n\n\n============ Entered ClearDemo() ==================\n\n\n")
		
		self.removeColorTags()
		self.clearTreeView()

		# First delete the Interpreted variables
		pragmaPackCurrentValue = None
		pragmaPackStack = []
		tokenLocationLinesChars = []
		variableDeclarations = []
		unraveled = []
		enums.clear()
		enumFieldValues.clear()
		typedefs.clear()
		structuresAndUnionsDictionary.clear()
		dummyVariableCount = 0
		totalVariableCount = 0
		globalScopes = []
		sizeOffsets = []
		variablesAtGlobalScopeSelected = []
		dataBlock = []

		# Then delete the code and data window variables
		codeFileName ="" 
		lines =[]
		dataFileName = ""
		dataBlock = []
		displayBlock = []

		# Then delete the code and data windows
		self.dataOffsetEntry.delete(0, tk.END)
		self.originalCodeText.delete("1.0", "end")
		self.interpretedCodeText.delete("1.0", "end")
		self.addressColumnText.delete("1.0", "end")
		self.viewDataHexText.delete("1.0", "end")
		self.viewDataAsciiText.delete("1.0", "end")
		if fileDisplayOffset != 0:
			self.fileOffset.set(0)
		if dataLocationOffset != 0:
			self.dataOffset.set(0)


if __name__ == "__main__":
	main()
