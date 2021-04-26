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
       | some compiler options are here.  Make your choice                          |
       |____________________________________________________________________________|
  
      -----------------------
     | Original code window  |
      -----------------------
  
     Here you either type/paste your C structure or variable declaration statements, or you can choose a code file.
     Do not put a .c file that contain other code that are not declarations (macro declarations are OK) as it will give errors.
     So, sanitize your input. Remove all code that is not related with variable declarations.
  
     Yes, this means a little more work on your part to figure out where all the declarations happened, where all the #defines are etc.
     But, this tool is not about finding those for you - rather, it depends on you being able to feed it the right declarations.
  
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
     The Coloring only happens if you "map" the code to the data on the right. So, using your cursor, make a selection.
     For all the variable names that fall within that selection, the tool will choose their global-level variables and map them onto the data. 
     For example, suppose you have structs like these defined below, if you just choose f_b, automatically the global-level variable varB
     will get selected, along with all the variables under it (basically i_b and f_b). Of course, varB is going to be overlapping the
     storage with both i_b and f_b, but that is essentially how structures work.
  
     There can be many, many combinations involving whether:
  
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
  
     (Neil Peart, their legendary drummer, died this January, hence this tribute)
  
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
    If you want to display your file from very specific offset, you can also type it in the Text Box to the right of "or".
    Here you can use human-readable expression, like 1MB-25KB+0xADE+(1<<10). Once you are done type, press TAB to focusout.
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
   
    This window has line-by-line listing of the different data items. And the listing is hierarchical.
    Which means, for items like Array and Structure, it will first show only one item - the Array or the Structure.
    But, if you then double-click on the item, or hit Enter, or press the Right-Arrow key, it will expand into Array elements or Structure members.
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
     - Compiler padding on or off - self-explanatory. When you Click this (turn it on or off), it will automatically re-interpret, and you will need to re-select
       your variables for mapping and press the "Map" button. Why we need to do this? Because when the compiler padding is turned on or off, ALL the size calculations
       go out of the window. The only way to do it properly is to start with a clean slate, by re-compiling.
     - Struct-end padding - when you turn on Compiler padding, this gives you a little more fine-grained control over whether you want to padding to apply AFTER the stuct end 
       or not. Similar to Compiler padding, we need to re-interpret after we make any changes here.
       Why we provide this separately? If two structures were part of the same source code, the compiler will surely add the requisite padding in between. 
       However, there might be cases where we are placing two structures from the different source in the final packet, and they are added contiguously 
       without any added padding in between.
     - Mapping Typedefs or not - Sometimes, in production there will be big structures that are typedefed. Now, when you just typedef a variable, the compiler does not create
       any storage for it since it is just a type. However, this means that the user will be forced to add a new line of code with a dummy variable name with the create type.
       To prevent that, I provided this option for counting typedefs too for structs.
       Also to remember - maybe you are using some typedefs that come as part of stdint.h (like uint32_t, uint16_t etc.). It is possible that your code uses a lot of
       these. However, the compiler here does not know what to make of those. In those cases, you have two options: 
         option A. Manually add the typedef statement like "typedef unsigned int uint32_t;" in your code.
         option B. If you are loathe to manually type the typedef statements and would rather do it for once and for all, there is a list inside this tool
         called typedefsBuiltin that already covers a few such cases (like int8_t, int16_t, int32_t, int64_t, uint8_t, uint16_t, uint32_t, uint64_t, intptr_t, uintptr_t).
         If your code uses some other typedefs frequently, maybe you can add them to this list.
     - Debug ON or OFF - when you turn the Debug on, it will start printing a massive amount of debug statements on the console. When you turn it off,
       it will invoke the dumpDetailsForDebug() routine that prints the most important lists and dictionaries used in this tool, and then turns it off.
       So, an easy way to see the internals of this tool for the current code is to turn the Debug ON and OFF right one after the other.
  
      --------------------------------------------------------------------
     | Running in BATCH mode                                              |
      --------------------------------------------------------------------
    
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
  
##       CROSS-PLATFORM STATUS: ##
  
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
  
    It was a royal pain in the ummm... neck porting it from Python 2 to Python 3. You see, at Intel the predominant Python version is 2.7,
    probably due to prevalence of PythonSV. I googled for changes between Python 2 and Python 3, and it seems reasonable. How wrong I was!!
  
    There are many, many subtle changes in Python 3 that will break your program written in Python 2. Some examples:
    - Your print used to be a statement, now it is a proper function
    - Your unicode and str were pretty much interchangeable. Now unicode is str, and str is bytes (Uggghhhhh!!)
    - Integer division - Python 2 would return an integer, but Python 3 would return a float
    - dict.key() used to generate a list, now it generates <<class dict_keys>>, so any code expecting it to be a list would fail silently
  
  
  
##       CURRENTLY WORK-IN-PROGRESS:  ##
    
    I am currently working on a few items. These items are not fully ready yet:
    - sizeof()
    - bitfield alignemnt for Big-Endian (cannot find a processor to test it).
  
##       KNOWN ISSUES:  ##
    
    This tool is first for me in many ways. 
  
        - This is my first Python program. 
        - This is my first compiler-writing. 
        - This is my first GUI development of any kind.
  
    And, I tested with it with EXACTLY ONE input file that contains some C declarations (that input is pasted right below README). Horrified enough?
  
    So, for a program that contains 8K lines of code, and has been tested for ONE test case, you can imagine the number of bugs it has!!!
  
    But, it is the age of outsourcing. So, ALL of you - the potential users - are my testers. I coded this FREE for you, you test this FREE for me. Win-Win!!
    Use it with your own test structures, and report to me anytime anything breaks (see below on how to report a bug).
  
    I know of an issue. For example, currently it does not handle the const/volatile/static etc. storage qualifier keywords very well.
    However, these storage qualifiers have absolutely no relevance for this too. So, feel free to delete them from your code and rerun it.
  
##       HOW  TO  REPORT  A  BUG:    ##
  
    Please email to Parbati.K.Manna@intel.com with a subject line of "ParseAndC bug" along with the following information/attachments:
  
    1. Your running environment (Windows / Unix / Mac), Python version.
    2. The input files you used for code and data. If the Data file is large, at least send the Code file. If you typed in the code, copy what you typed.
    3. your Data Offset and File Offset values for which it is breaking.
    4. Turn on the debug setting on this tool by clicking on the "Debug" button . When you do that, the tool will become slow, and it will print a
       whole lot of debug messages on the background console. This is the most useful debugging information, so please capture that and attach it.
  
  
##       FEEDBACK PLEASE!!!!      ##
  
    if you like this tool, I want to hear about it.
    If you feel that this tool sucks, I still want to hear about it.
    If you have some feature in mind that you feel would make the tool better, I want to hear about it.
  
    Please email me with any feedback: Parbati.K.Manna@intel.com
  
