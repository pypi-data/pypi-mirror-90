define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
 
    , './api.js'
    , './constData.js'
    , './component/base/index.js'
 ], function ( vpCommon, sb, 
                api, constData, baseComponent ) {
 
    const { DeleteOneArrayValueAndGet
            , IsCodeBlockType
            , MapNewLineStrToIndentString } = api;
 
    const { BLOCK_CODELINE_TYPE
            , IMPORT_BLOCK_TYPE
            , IF_BLOCK_CONDITION_TYPE
            , FOCUSED_PAGE_TYPE
            
            , DEF_BLOCK_ARG4_TYPE

            , FOR_BLOCK_ARG3_TYPE
            , WHILE_BLOCK_TYPE 

            , NUM_FONT_WEIGHT_300
            , NUM_FONT_WEIGHT_700
 
            , STR_NULL
            , STR_DIV
            , STR_SELECTED
            , STR_ONE_SPACE
            , STR_ONE_INDENT
            , STR_CHECKED
            
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
 
            , STR_INPUT_YOUR_CODE
            , STR_ICON_ARROW_UP
            , STR_ICON_ARROW_DOWN
            , STR_BORDER 
            , STR_DEFAULT
            , STR_CUSTOM
            , STR_TRANSPARENT
 
            , STR_FONT_WEIGHT
            , STR_BORDER_RIGHT
            , STR_BORDER_TOP_LEFT_RADIUS
            , STR_BORDER_BOTTOM_LEFT_RADIUS
            , STR_BORDER_TOP_RIGHT_RADIUS
            , STR_BORDER_BOTTOM_RIGHT_RADIUS
            , STR_3PX
            , STR_SOLID
            , STR_COLOR
            , STR_BACKGROUND_COLOR
            , STR_CLICK
            , STR_COLON_SELECTED
            , STR_CHANGE_KEYUP_PASTE
            , STR_KEYWORD_NEW_LINE

            , VP_ID_PREFIX 
            , VP_ID_APIBLOCK_LEFT_TAP_APILIST_PAGE

            , VP_CLASS_PREFIX 
 
            , VP_BLOCK_BLOCKCODELINETYPE_CODE
            , VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF
            , VP_BLOCK_BLOCKCODELINETYPE_CONTROL
 
            , VP_CLASS_BLOCK_CODETYPE_NAME
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED
            , VP_CLASS_APIBLOCK_PARAM_PLUS_BTN
 
            , STATE_classInParamList
            , STATE_className
            , STATE_parentClassName
            
            , STATE_defName
            , STATE_defInParamList
            , STATE_defReturnType

            , STATE_ifCodeLine
            , STATE_isIfElse
            , STATE_isForElse
            , STATE_ifConditionList
            , STATE_elifConditionList
 
            , STATE_elifCodeLine
            , STATE_elifList
 
            , STATE_forCodeLine
            , STATE_forParam 
            , STATE_listforConditionList
            , STATE_listforReturnVar
            , STATE_listforPrevExpression
 
            , STATE_whileCodeLine
            , STATE_whileBlockOptionType
            , STATE_whileArgs
            , STATE_whileConditionList

            , STATE_breakCodeLine
            , STATE_passCodeLine
            , STATE_continueCodeLine
 
            , STATE_baseImportList
            , STATE_customImportList
 
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_exceptConditionList
 
            , STATE_isFinally
 
            , STATE_returnOutParamList
 
            , STATE_codeLine
 
            , STATE_propertyCodeLine
 
            , STATE_commentLine
 
            , STATE_lambdaArg1
            , STATE_lambdaArg2List
            , STATE_lambdaArg2m_List
            , STATE_lambdaArg3
            , STATE_lambdaArg4List
 
            , COLOR_GRAY_input_your_code
            , COLOR_FOCUSED_PAGE
            , COLOR_BLACK } = constData;
    const {  } = baseComponent;  

    var RenderBlockMainDom = function(thatBlock) {
        var mainDom = document.createElement(STR_DIV);
        mainDom.classList.add('vp-block');
        mainDom.classList.add(`vp-block-${thatBlock.getUUID()}`);

        var blockCodeLineType = thatBlock.getBlockCodeLineType()
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.NODE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.TEXT) {
            $(mainDom).css('margin-top', 20);
        }
  
        return mainDom;
    }
    
    var RenderBlockLeftHolderDom = function(thatBlock) {
        var mainDom = document.createElement(STR_DIV);
        mainDom.classList.add('vp-block-left-holder');

        return mainDom;
    }
 
    var RenderBlockMainInnerDom = function(thatBlock) {
        var mainInnerDom = $(`<div class='vp-block-inner'></div>`);
        mainInnerDom.attr("id", `vp_block-${thatBlock.getUUID()}`);
        return mainInnerDom;
    }
 
    /** class param 생성 */
    var GenerateClassInParamList = function(thatBlock) {
        var parentClassName = thatBlock.getState(STATE_parentClassName);
        var classInParamStr = `(`;
        classInParamStr += parentClassName;
        classInParamStr += `):`;
        return classInParamStr;
    }
 
    /** def param 생성 */
    var GenerateDefInParamList = function(thatBlock) {
         /** 함수 파라미터 */
         var defInParamList = thatBlock.getState(STATE_defInParamList);
         var defReturnTypeState = thatBlock.getState(STATE_defReturnType);
         var defInParamStr = `(`;
         defInParamList.forEach(( defInParam, index ) => {
             const { arg3, arg4, arg5 ,arg6 } = defInParam;
            //  if (arg3 !== '' ) {
                 
                 if (arg6 == '*args') {
                     defInParamStr += '*';
                 } else if (arg6 == '**kwargs') {
                     defInParamStr += '**';
                 }
 
                 defInParamStr += arg3;
 
                 if (arg4 == DEF_BLOCK_ARG4_TYPE.NONE || arg4 == STR_NULL) {
                    defInParamStr += '';
                 } else {
                   
                    if (arg4 != DEF_BLOCK_ARG4_TYPE.INPUT_STR) {
                        defInParamStr += ':';
                        defInParamStr += arg4;
                    } 
                    // else {
                    //     defInParamStr += ':';
                    //     defInParamStr += arg4;
                    // }
                 }
 
                 if (arg5 !== '') {
                     defInParamStr += `=${arg5}`;
                 }
 
                 for (var i = index + 1; i < defInParamList.length; i++) {
                     if (defInParamList[i].arg3 !== '') {
                         defInParamStr += `, `;
                         break;
                     }
                 };
            //  }
         });
         defInParamStr += `)`;

         if (defReturnTypeState == DEF_BLOCK_ARG4_TYPE.NONE || defReturnTypeState == STR_NULL) {
            defInParamStr += `:`;
         } else {
            if (defReturnTypeState != DEF_BLOCK_ARG4_TYPE.INPUT_STR) {
                defInParamStr += ` `;
                defInParamStr += `->`;
                defInParamStr += ` `;
                defInParamStr += defReturnTypeState;
                defInParamStr += `:`;
            } 
            // else {

            // }

         }
 
         return defInParamStr;
    }
 
    /** return param 생성 */
    var GenerateReturnOutParamList = function(thatBlock) {
        var returnOutParamList = thatBlock.getState(STATE_returnOutParamList);
        var returnOutParamStr = ` `;
        returnOutParamList.forEach(( returnInParam, index ) => {
            if (returnInParam !== '' ) {
                returnOutParamStr += `${returnInParam}`;
                for (var i = index + 1; i < returnOutParamList.length; i++) {
                    if (returnOutParamList[i] !== '') {
                        returnOutParamStr += `, `;
                        break;
                    }
                };
            }
        });
        returnOutParamStr += ``;
        return returnOutParamStr;
    }
 
    /** if param 생성 */
    var GenerateIfConditionList = function(thatBlock, blockCodeLineType) {
         var ifConditionList;
         if (blockCodeLineType == BLOCK_CODELINE_TYPE.IF) {
             ifConditionList = thatBlock.getState(STATE_ifConditionList);
         } else {
             ifConditionList = thatBlock.getState(STATE_elifConditionList);
         }
 
         var ifConditionListStr = ``;
         ifConditionList.forEach(( ifCondition, index ) => {
             const { conditionType } = ifCondition;
             if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                const { arg1, arg2, arg3, arg4, arg5, arg6 } = ifCondition;

                if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                    ifConditionListStr += `(`;
                }
                ifConditionListStr += arg1;
  
                if ( arg2 !== 'none' ) {
                    ifConditionListStr += arg2;
                }
                ifConditionListStr += arg3;
         
                if ( arg4 !== 'none' ) {
                    ifConditionListStr += arg4;
                    ifConditionListStr += arg5;
                }
                 
                if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                    ifConditionListStr += `)`;
                }
         
                if ( ifConditionList.length -1 !== index ) {
                    ifConditionListStr += '';
                    ifConditionListStr += arg6;
                    ifConditionListStr += '';
                }
            } else {
                const { codeLine, arg6 } = ifCondition;
                if (codeLine == '') {
                    return;
                }
                ifConditionListStr += `(`;
                ifConditionListStr += codeLine;
                ifConditionListStr += `)`;
 
                if ( ifConditionList.length -1 !== index ) {
                    ifConditionListStr += '';
                    ifConditionListStr += arg6;
                    ifConditionListStr += '';
                }
            }
        });
 
        return ifConditionListStr;
    }
 
      /** while param 생성 */
    var GenerateWhileConditionList = function(thatBlock) {
        var ifConditionList = thatBlock.getState(STATE_whileConditionList);
 

        var ifConditionListStr = ``;
        ifConditionList.forEach(( ifCondition, index ) => {
            // const { conditionType } = ifCondition;
            // if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                const { arg1, arg2, arg3, arg4, arg5, arg6 } = ifCondition;

               if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                   ifConditionListStr += `(`;
               }

                ifConditionListStr += arg1;
 
                if ( arg2 !== 'none' ) {
                   ifConditionListStr += arg2;
                }
                ifConditionListStr += arg3;
        
                if ( arg4 !== 'none' ) {
                    ifConditionListStr += arg4;
                    ifConditionListStr += arg5;
                }
                
                if ( !(arg1 == '' && (arg2 == 'none' || arg2 == '') && arg3 == '')) {
                   ifConditionListStr += `)`;
               }
        
                if ( ifConditionList.length -1 !== index ) {
                    ifConditionListStr += '';
                    ifConditionListStr += arg6;
                    ifConditionListStr += '';
                }
            // } else {
                // const { codeLine, arg6 } = ifCondition;
                // if (codeLine == '') {
                //     return;
                // }
                // ifConditionListStr += `(`;
                // ifConditionListStr += codeLine;
                // ifConditionListStr += `)`;

                // if ( ifConditionList.length -1 !== index ) {
                //     ifConditionListStr += '';
                //     ifConditionListStr += arg6;
                //     ifConditionListStr += '';
                // }
            // }

        });

       return ifConditionListStr;
    }
     var GenerateExceptConditionList = function(thatBlock) {
         var exceptConditionList = thatBlock.getState(STATE_exceptConditionList);
 
         var exceptConditionListStr = ``;
         exceptConditionList.forEach(( exceptCondition, index ) => {
            const { conditionType } = exceptCondition;
            if (conditionType == IF_BLOCK_CONDITION_TYPE.ARG) {
                const { arg1, arg2, arg3 } = exceptCondition;
        
                exceptConditionListStr += arg1;

                if ( arg2 == 'none' || arg2 == STR_NULL ) {
                } else {
                    exceptConditionListStr += ' ';
                    exceptConditionListStr += arg2;
                    exceptConditionListStr += ' ';
                    exceptConditionListStr += arg3;
                }
        
            } else {
                const { codeLine } = exceptCondition;
                if (codeLine == '') {
                    return;
                }
             
                exceptConditionListStr += codeLine;
            }
     
         });
 
        return exceptConditionListStr;
     }
 
     /** for param 생성 */
     var GenerateForParam = function(thatBlock) {
         var forParam = thatBlock.getState(STATE_forParam);
         const { arg1, arg2, arg3, arg4, arg5, arg6, arg7 } = forParam;
 
         var forParamStr = ``;
 
         if (arg1 !== STR_NULL) {
             forParamStr += arg1;
             forParamStr += ' ';
         }
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE && arg1 !== STR_NULL && arg4 !== STR_NULL) { 
             forParamStr += ',';
         }
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ENUMERATE && arg4 !== STR_NULL) {
             forParamStr += arg4;
             forParamStr += ' ';
         }
 
         forParamStr += 'in';
         forParamStr += ' ';
 
         if (arg3 == FOR_BLOCK_ARG3_TYPE.ZIP) {
             forParamStr += arg3;
             forParamStr += '(';
             forParamStr += arg2;
 
             if (arg7 !== '') {
                 forParamStr += ',';
                 forParamStr += ' ';
                 forParamStr += arg7;
             }
 
             forParamStr += ')';
 
         } else if (arg3 ==  FOR_BLOCK_ARG3_TYPE.ENUMERATE ) {
             forParamStr += arg3;
             forParamStr += '(';
             forParamStr += arg2;
             forParamStr += ')';
 
         } else if (arg3 ==  FOR_BLOCK_ARG3_TYPE.RANGE ) {
             forParamStr += arg3;
             forParamStr += '(';
 
             if (arg5 !== '') {
                 forParamStr += arg5;
             }
 
             if (arg5 !== '' && arg2 !== '') { 
                 forParamStr += ',';
             }
 
             if (arg2 !== '') {
                 forParamStr += ' ';
                 forParamStr += arg2;
             }
 
             if ((arg5 !== '' || arg2 !== '') && arg6 !== '') { 
                 forParamStr += ',';
             }
 
             if (arg6 !== '') {
                 forParamStr += ' ';
                 forParamStr += arg6;
             }
   
             forParamStr += ')';
 
         } else {
            if (arg3 != FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                forParamStr += arg3;
            } 

            if (arg2 != '') {
                if (arg3 == '' || arg3 == FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                    forParamStr += arg2;
                } else {
                    forParamStr += '(';
                    forParamStr += arg2;
                    forParamStr += ')';
                }
            }

         }

         return forParamStr;
     }
 
     /** Listfor param 생성 */
     var GenerateListforConditionList = function(thatBlock) {
         var listforStr = '';
         var listforReturnVar = thatBlock.getState(STATE_listforReturnVar);
         var listforPrevExpression = thatBlock.getState(STATE_listforPrevExpression);
 
         if (listforReturnVar != '') {
             listforStr += listforReturnVar;
             listforStr += ' ';
             listforStr += '=';
             listforStr += ' ';
         }
 
         listforStr += '[';
         listforStr += listforPrevExpression;
 
 
         var listforConditionList = thatBlock.getState(STATE_listforConditionList);
         listforConditionList.forEach(listforCondition => {
            //  console.log('listforCondition',listforCondition);
             const { arg1, arg2, arg3, arg4, arg5, arg6, arg7
                     , arg10, arg11, arg12, arg13, arg14, arg15  } = listforCondition;
 
             listforStr += ' ';
             listforStr += 'for';
             listforStr += ' ';
             if (arg1 !== '') {
                 listforStr += arg1;
                 listforStr += ' ';
             }
     
             if (arg3 == 'enumerate' && arg1 !== '' && arg4 !== '') { 
                 listforStr += ',';
             }
     
             if (arg3 == 'enumerate' && arg4 !== '') {
                 listforStr += arg4;
                 listforStr += ' ';
             }
     
             listforStr += 'in';
             listforStr += ' ';
     
             if (arg3 == 'zip') {
                 listforStr += arg3;
                 listforStr += '(';
                 listforStr += arg2;
     
                 if (arg7 !== '') {
                     listforStr += ',';
                     listforStr += ' ';
                     listforStr += arg7;
                 }
     
                 listforStr += ')';
     
             } else if (arg3 == 'enumerate') {
                 listforStr += arg3;
                 listforStr += '(';
                 listforStr += arg2;
                 listforStr += ')';
     
             } else if (arg3 == 'range') {
                 listforStr += arg3;
                 listforStr += '(';
     
                 if (arg5 !== '') {
                     listforStr += arg5;
                 }
     
                 if (arg5 !== '' && arg2 !== '') { 
                     listforStr += ',';
                 }
     
                 if (arg2 !== '') {
                     listforStr += ' ';
                     listforStr += arg2;
                 }
     
                 if ((arg5 !== '' || arg2 !== '') && arg6 !== '') { 
                     listforStr += ',';
                 }
     
                 if (arg6 !== '') {
                     listforStr += ' ';
                     listforStr += arg6;
                 }
       
                 listforStr += ')';
     
             } 

            else {
                if (arg3 != FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                    listforStr += arg3;
                } 
    
                if (arg2 != '') {
                    if (arg3 == '' || arg3 == FOR_BLOCK_ARG3_TYPE.INPUT_STR) {
                        listforStr += arg2;
                    } else {
                        listforStr += '(';
                        listforStr += arg2;
                        listforStr += ')';
                    }
                }
    
             }
 
             if (arg10 == 'if') {
                 listforStr += ' ';
                 listforStr += 'if';
                 listforStr += ' ';
                 listforStr += `(`;
         
                 listforStr += arg11;
                 listforStr += arg12;
                 listforStr += arg13;
         
                 if ( arg14 !== 'none' ) {
                     listforStr += arg14;
                     listforStr += arg15;
                 }
                 
                 listforStr += ' ';
                 listforStr += `)`;
                 listforStr += '';
     
             } else if (arg10 == 'inputStr') {
 
             }
         });
 
         listforStr += ']';
         return listforStr;
     }
 
     var GenerateLambdaParamList = function(thatBlock) {
         var lambdaParamStr = STR_NULL;
         var lambdaArg1State = thatBlock.getState(STATE_lambdaArg1);
         var lambdaArg2ListState = thatBlock.getState(STATE_lambdaArg2List);
         var lambdaArg2m_ListState = thatBlock.getState(STATE_lambdaArg2m_List);
         var lambdaArg3State = thatBlock.getState(STATE_lambdaArg3);
         var lambdaArg4ListState = thatBlock.getState(STATE_lambdaArg4List);
         if (lambdaArg1State != '') {
             lambdaParamStr += lambdaArg1State;
             lambdaParamStr += ' ';
             lambdaParamStr += '=';
             lambdaParamStr += ' ';
         }
    
  
         lambdaArg4ListState.forEach( (lambdaArg4, index) => {
             lambdaParamStr += lambdaArg4;
             lambdaParamStr += '(';
         });
 
         lambdaParamStr += 'lambda';
         lambdaParamStr += ' ';
         lambdaArg2ListState.forEach( (lambdaArg2, index) => {
             lambdaParamStr += lambdaArg2;
             if ( lambdaArg2ListState.length - 1 != index) {
                 if (lambdaArg2 != '') {
                    lambdaParamStr += ' ';
                    lambdaParamStr += ',';
                 }
             }
         });
   
         lambdaParamStr += ':';
       
         lambdaParamStr += MapNewLineStrToIndentString(lambdaArg3State);
     
         lambdaParamStr += ',';
         lambdaArg2m_ListState.forEach( (lambdaArg2_m, index) => {
             lambdaParamStr += lambdaArg2_m;
             if ( lambdaArg2m_ListState.length - 1 != index) {
                if (lambdaArg2_m != '') {
                    lambdaParamStr += ' ';
                    lambdaParamStr += ',';
                 }
             }
         });
         lambdaArg4ListState.forEach( (lambdaArg4, index) => {
             lambdaParamStr += ')';
         });
   
         return lambdaParamStr;
     }

     var GenerateImportList = function(thisBlock, indentString) {
        var codeLine = STR_NULL;
        var blockName = 'import';
        var baseImportList = thisBlock.getState(STATE_baseImportList).filter(baseImport => {
            if ( baseImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });

        var customImportList = thisBlock.getState(STATE_customImportList).filter(customImport => {
            if ( customImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });
   
        var lineNum = 0;
        var indentString = thisBlock.getIndentString();

        baseImportList.forEach((baseImport, index) => {
            if (lineNum > 0) {
                codeLine += indentString;
            } 
      
            codeLine += `${blockName.toLowerCase()} ${baseImport.baseImportName} as ${baseImport.baseAcronyms}`;
            if (baseImport.baseImportName == 'matplotlib.pyplot') {
                codeLine += STR_KEYWORD_NEW_LINE;
                codeLine += indentString;
                codeLine += `%matplotlib inline`;
            }

            if (index != baseImportList.length - 1) {
                codeLine += STR_KEYWORD_NEW_LINE;
            }
            lineNum++;
        });

        customImportList.forEach((customImport,index ) => {
            if (lineNum > 0) {
                codeLine += indentString;
            } 

            codeLine += `${blockName.toLowerCase()} ${customImport.baseImportName} as ${customImport.baseAcronyms}`;
            if (customImport.baseImportName == 'matplotlib.pyplot') {
                codeLine += STR_KEYWORD_NEW_LINE;
                codeLine += indentString;
                codeLine += `%matplotlib inline`;
            }

            if (index != customImportList.length - 1) {
                codeLine += STR_KEYWORD_NEW_LINE;
            }

            lineNum++;
        });

        // console.log(codeLine);
        return codeLine;
     };

     var GenerateWhileBlockCode = function(thisBlock) {
        var whileBlockCode = STR_NULL;
        var whileArgsState = thisBlock.getState(STATE_whileArgs)
        var whileBlockOptionType = thisBlock.getState(STATE_whileBlockOptionType);
        const { arg1, arg2, arg3, arg4, arg5 } = whileArgsState;

        if (whileBlockOptionType == WHILE_BLOCK_TYPE.CONDITION) {
            whileBlockCode += arg4;
            whileBlockCode += arg2;
            whileBlockCode += arg3;
        } else if (whileBlockOptionType == WHILE_BLOCK_TYPE.TRUE_FALSE) {
            whileBlockCode += arg1;
        } else {
            whileBlockCode += arg1;
        }
        return whileBlockCode;
     }

     var ShowImportListAtBlock = function(thisBlock) {
        var codeLine = STR_NULL;
        // var blockName = 'import';
        var baseImportList = thisBlock.getState(STATE_baseImportList).filter(baseImport => {
            if ( baseImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });
        var customImportList = thisBlock.getState(STATE_customImportList).filter(customImport => {
            if ( customImport.isImport == true) {
                return true;
            } else {
                return false;
            }
        });

        if (baseImportList.length != 0) {
            codeLine += baseImportList[0].baseImportName + ' as ' + baseImportList[0].baseAcronyms;
        } else if (customImportList.length != 0) {
            codeLine += customImportList[0].baseImportName + ' as ' + customImportList[0].baseAcronyms;
        }
        return codeLine;
    }
    
    /**  멀티라인의 첫번째 줄만 보여준다 */
    var ShowCodeBlockCode = function(thisBlock) {
        var codeLine = thisBlock.getState(STATE_codeLine);
        var firstNewLine_index = codeLine.indexOf('\n');
        if (firstNewLine_index != -1) {
            var sliced_codeline = codeLine.slice(0, firstNewLine_index);
            return sliced_codeline;
        } else {
            return codeLine;
        }
    }
    

     /** TODO: blockCodeLine type에 따라 css를 다르게 해야 함 */
    var RenderBlockMainHeaderDom = function(thatBlock) {

        var blockCodeLineType =  thatBlock.getBlockCodeLineType();

        /** class 이름 */
        var className = thatBlock.getState(STATE_className);
        var classInParamStr = GenerateClassInParamList(thatBlock);
 
        /** def 이름 */
        var defName = thatBlock.getState(STATE_defName);
        var defInParamStr = GenerateDefInParamList(thatBlock);
        
        var codeStr = '';
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.IF) {
            codeStr = GenerateIfConditionList(thatBlock, BLOCK_CODELINE_TYPE.IF);
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF) {
            codeStr = GenerateIfConditionList(thatBlock, BLOCK_CODELINE_TYPE.ELIF);
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.FOR) {
            codeStr = GenerateForParam(thatBlock);
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE) {
            codeStr = GenerateWhileConditionList(thatBlock);
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT) {
            codeStr = GenerateExceptConditionList(thatBlock);
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.RETURN) {
            codeStr = GenerateReturnOutParamList(thatBlock);
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA) {
            codeStr = GenerateLambdaParamList(thatBlock);
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT) {
            codeStr = ShowImportListAtBlock(thatBlock);
        }

        var blockName = thatBlock.getBlockName();
        /** true면 Block이 board에서 이름이 표시되지 않는다. */
        var isBlockNameShow = true;
        var blockSymbol = '';
        if ( IsCodeBlockType(blockCodeLineType) == true 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA
            || blockCodeLineType == BLOCK_CODELINE_TYPE.NODE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.TEXT
            || blockCodeLineType == BLOCK_CODELINE_TYPE.API) {
            isBlockNameShow = false;
        }
 
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY) {
            blockSymbol = '@';
            isBlockNameShow = false;
        }
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.COMMENT) {
            blockSymbol = '#';
            isBlockNameShow = false;
        }
 
        var blockUUID = thatBlock.getUUID();
        var mainHeaderDom;
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.TEXT ) {
            mainHeaderDom =`<div class='vp-block-header'
                                 style='height:unset;'>
                                <div id='vp_block-${blockUUID}'
                                    class='vp-block-header-${blockUUID}'
                                    style='font-size:12px;'>
                                    ${thatBlock.getState(STATE_codeLine)}
                                </div>
                         
                            </div>
                            `
        } else {
            mainHeaderDom = $(`<div class='vp-block-header'>
                                ${
                                    isBlockNameShow == true
                                        ? `<strong class='vp-apiblock-style-flex-column-center 
                                            ${thatBlock.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER 
                                                                                ? VP_CLASS_BLOCK_CODETYPE_NAME
                                                                                : ''}' 
                                                id='vp_block-${blockUUID}'
                                                style='margin-right:30px; 
                                                        font-size:12px; 
                                                        color:#252525;
                                                        font-weight: 700;
                                                        font-family: Consolas;'>
                                            ${blockName}
                                            </strong>`
                                        : `<strong class='vp-apiblock-style-flex-column-center' 
                                            id='vp_block-${blockUUID}'
                                                style='font-size:12px; 
                                                        color:#252525;
                                                        font-weight: 700;
                                                        font-family: Consolas;'>
                                            ${blockSymbol}
                                            </strong>`
                                }
                                <div id='vp_block-${blockUUID}' 
                                    class='vp-apiblock-codeline-ellipsis 
                                            vp-apiblock-codeline-container-box'
                                    style='${blockCodeLineType == BLOCK_CODELINE_TYPE.NODE 
                                                ? 'background-color:white;' 
                                                : ''}'>

                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS   
                                                ? `<div id='vp_block-${blockUUID}' 
                                                        class='vp-apiblock-style-flex-row'>
                                                        <div id='vp_block-${blockUUID}'
                                                            class='vp-block-header-class-name-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${className}
                                                        </div>
                                                        <div id='vp_block-${blockUUID}'
                                                            class='vp-block-header-param
                                                                    vp-block-header-param-${blockUUID}'
                                                            style='font-size:12px;
                                                                   text-indent: 0em;'>
                                                            ${classInParamStr}
                                                        </div>
                                                    </div>`
                                                : STR_NULL
                                        }

                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.DEF  
                                                ? `<div id='vp_block-${blockUUID}'
                                                        class='vp-apiblock-style-flex-row'>
                                                        <div id='vp_block-${blockUUID}'
                                                            class='vp-block-header-def-name-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${defName}
                                                        </div>
                                                        <div id='vp_block-${blockUUID}'
                                                            class='vp-block-header-param
                                                                    vp-block-header-${blockUUID}'
                                                                style='font-size:12px; 
                                                                       text-indent: 0em;'>
                                                                ${defName.length == 0 
                                                                    ? ''
                                                                    : defInParamStr}
                                                        </div>
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.IF    
                                            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR 
                                            || blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
                                            || blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE 
                                            || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT
                                            || blockCodeLineType == BLOCK_CODELINE_TYPE.RETURN  
                                            || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA 
                                            || blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT 
                                                ? `<div id='vp_block-${blockUUID}'
                                                        class='vp-block-header-param
                                                            vp-block-header-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${codeStr}
                                                    </div>`
                                                : STR_NULL
                                        }     
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.API 
                                                ?`<div id='vp_block-${blockUUID}'
                                                    class='vp-block-header-param
                                                        vp-block-header-${blockUUID}'
                                                    style='font-size:12px;'>
                                                    ${thatBlock.getState(STATE_codeLine)}
                                                </div>`
                                                : STR_NULL
                                        }
                                        ${
                                        blockCodeLineType == BLOCK_CODELINE_TYPE.BREAK  
                                        || blockCodeLineType == BLOCK_CODELINE_TYPE.CONTINUE  
                                        || blockCodeLineType == BLOCK_CODELINE_TYPE.PASS 
                                        || blockCodeLineType == BLOCK_CODELINE_TYPE.CODE  
                                        || blockCodeLineType == BLOCK_CODELINE_TYPE.COMMENT 
                                        || blockCodeLineType == BLOCK_CODELINE_TYPE.PRINT
                                        || blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY
                                                ? `<div id='vp_block-${blockUUID}'
                                                        class='vp-block-header-param
                                                            vp-block-header-${blockUUID}'
                                                        style='font-size:12px; 
                                                            color:${ShowCodeBlockCode(thatBlock) == STR_NULL 
                                                                            ? `${COLOR_GRAY_input_your_code}` 
                                                                            : ''};'>
                                                        ${ShowCodeBlockCode(thatBlock) == STR_NULL
                                                            ? STR_INPUT_YOUR_CODE
                                                            : ShowCodeBlockCode(thatBlock)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                    
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK        
                                                ? `<div id='vp_block-${blockUUID}'
                                                        style='background-color:transparent;'>
                                                    </div>`
                                                : STR_NULL
                                        }    
                                        ${
                                            blockCodeLineType == BLOCK_CODELINE_TYPE.NODE
                                                ? `<div id='vp_block-${blockUUID}'
                                                        class='vp-apiblock-nodeblock'>
                                                        <div id="vp_apiblock_nodeblock_${blockUUID}"
                                                            class='vp-block-header-param
                                                                    vp-block-header-${blockUUID}
                                                                    vp-apiblock-nodeblock-${blockUUID}
                                                                    vp-apiblock-style-flex-row'
                                                            style='font-size:12px; '>

                                                            <div class='vp-apiblock-nodeblock-text'>
                                                                ${ShowCodeBlockCode(thatBlock)}
                                                            </div>

                                                            <div class='vp-apiblock-nodeblock-blank'>
                                                            </div>

                                                        </div>

                                                        <input 
                                                            style="display:none;"
                                                            class="vp-apiblock-nodeblock-input
                                                                   vp-apiblock-nodeblock-input-${blockUUID}"
                                                            id="vp_apiblock_nodeblock_input_${blockUUID}"
                                                            value='${ShowCodeBlockCode(thatBlock)}'>
                                                        </input>
                                                    </div>`
                                                : STR_NULL  
                                        }
                                        </div>
                                </div>`);
        }
        return mainHeaderDom;
    }  

 
    /** 특정 input태그 값 입력 안 될시 빨간색 border 
     */
    var RenderInputRequiredColor = function(thatBlock) {
        if ($(thatBlock).val() == STR_NULL) {
            $(thatBlock).addClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED)
        } else {
            $(thatBlock).removeClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED); 
        }
    }
 
    var RenderSelectRequiredColor = function(target, selectedValue) {
        if (selectedValue == STR_NULL) {
            $(target).addClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED)
        } else {
            $(target).removeClass(VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED); 
        }
    }
 
    var RenderDeleteBlockButton = function() {
        var deleteBtn = $(`<div class='vp-block-delete-btn
                                       vp-apiblock-style-flex-column-center'>
                                <i class="vp-fa fa fa-times vp-block-option-icon"></i>
                            </div>`);
        return deleteBtn;                     
    }
 
    var RenderFocusedPage = function(focusedPageType) {
 
    }
 
    /**
     * @param {string} inputValue 
     */
    var RenderCodeBlockInputRequired = function(thisBlock, inputValue, state) {
        /** 어떤 데이터도 입력되지 않을 때 */
        // var thisBlock = this;
        if (inputValue == STR_NULL) {
            thisBlock.writeCode(STR_INPUT_YOUR_CODE);
            $(`.vp-block-header-${thisBlock.getUUID()}`).css(STR_COLOR, COLOR_GRAY_input_your_code);
            return;
        }
 
        /** 데이터가 입력되었을 때 */
        thisBlock.writeCode(state);
        $(`.vp-block-header-${thisBlock.getUUID()}`).css(STR_COLOR, COLOR_BLACK);
    }
 
     var RenderHTMLDomColor = function(block, htmlDom) {
         var blockCodeLineType = block.getBlockCodeLineType()
 
         /** class & def 블럭 */
         if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);
             
         /** controls 블럭 */
         } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR
             || blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY
             || blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
             || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY 
             || blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT
             || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA
             || blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY ) {
                 
             //  COLOR_CONTROL;
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CONTROL);
 
         } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK){
             $(htmlDom).css('background-color', 'transparent !important');
    
         }  else if (blockCodeLineType == BLOCK_CODELINE_TYPE.TEXT) {
            $(htmlDom).css(STR_BACKGROUND_COLOR,'transparent !important');
         } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.HOLDER ) {

         } else {
             $(htmlDom).addClass(VP_BLOCK_BLOCKCODELINETYPE_CODE);
         }
         return htmlDom;
    }
 
    return {
        RenderBlockMainDom
        , RenderBlockLeftHolderDom
        , RenderBlockMainInnerDom
        , RenderBlockMainHeaderDom
 
        , RenderDeleteBlockButton
        , RenderFocusedPage
 
        , RenderInputRequiredColor
        , RenderSelectRequiredColor
     
        , RenderCodeBlockInputRequired
        
        , RenderHTMLDomColor
 
        , GenerateClassInParamList
        , GenerateDefInParamList
        , GenerateReturnOutParamList
        , GenerateIfConditionList
        , GenerateExceptConditionList
        , GenerateForParam
        , GenerateListforConditionList
        , GenerateLambdaParamList
        , GenerateImportList
        , GenerateWhileBlockCode
        , GenerateWhileConditionList

        , ShowImportListAtBlock
        , ShowCodeBlockCode
    }
 });
 