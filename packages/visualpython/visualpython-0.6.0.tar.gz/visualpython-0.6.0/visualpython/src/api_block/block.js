define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    , './api.js'
 
    , './constData.js'

    , './blockRenderer.js'

    , './component/option/class_option.js'
    , './component/option/def_option.js'
    , './component/option/if_option.js'
    , './component/option/elif_option.js'  
    , './component/option/else_option.js'  

    , './component/option/try_option.js'
    , './component/option/except_option.js'  
    , './component/option/for_option.js'
    , './component/option/listfor_option.js'

    , './component/option/import_option.js'  

    , './component/option/code_option.js'

    , './component/option/return_option.js'
    , './component/option/while_option.js'
    , './component/option/lambda_option.js'

    , './component/option/sample_option.js'
    , './component/option/api_option.js'

    , './component/option/text_option.js'
    , './component/option/node_option.js'
], function ( vpCommon, vpFuncJS 
    
              , api 
    
              , constData 
            
              , blockRenderer

              , InitClassBlockOption
              , InitDefBlockOption
              , InitIfBlockOption
              , InitElifBlockOption
              , InitElseBlockOption

              , InitTryBlockOption
              , InitExceptBlockOption
              , InitForBlockOption
              , InitListForBlockOption

              , InitImportBlockOption

              , InitCodeBlockOption

              , InitReturnBlockOption
              , InitWhileBlockOption
              , InitLambdaBlockOption
              
              , InitSampleBlockOption 
              , InitApiBlockOption

              , InitTextBlockOption
              , InitNodeBlockOption) {

    // const ShadowBlock = shadowBlock;

    const { ChangeOldToNewState
            , FindStateValue

            , DestructureFromBlockArray

            , MakeFirstCharToUpperCase
            , MapTypeToName

            , MapNewLineStrToIndentString
            , IsCanHaveIndentBlock } = api;

    const { RenderHTMLDomColor
            , GenerateClassInParamList
            , GenerateDefInParamList
            , GenerateReturnOutParamList
            , GenerateIfConditionList
            , GenerateForParam
            , GenerateListforConditionList
            , GenerateLambdaParamList
            , GenerateExceptConditionList
            , GenerateImportList
            , GenerateWhileConditionList } = blockRenderer;

    const { BLOCK_CODELINE_TYPE
                , BLOCK_DIRECTION
                , BLOCK_TYPE
                , FOCUSED_PAGE_TYPE
    
                , DEF_BLOCK_ARG4_TYPE
                , FOR_BLOCK_TYPE
                , FOR_BLOCK_ARG3_TYPE
                
             
                , IF_BLOCK_CONDITION_TYPE
    
                , NUM_BLOCK_HEIGHT_PX
                , NUM_INDENT_DEPTH_PX
                , NUM_MAX_ITERATION
    
                , NUM_DEFAULT_BLOCK_LEFT_HOLDER_HEIGHT
    
                , NUM_EXCEED_DEPTH
     
                , NUM_BLOCK_BOTTOM_HOLDER_HEIGHT
                , NUM_TEXT_BLOCK_WIDTH
    
                , STR_NULL
                , STR_TOP
                , STR_LEFT
                , STR_BORDER
                , STR_BORDER_LEFT
                , STR_PX
                , STR_OPACITY
                , STR_MARGIN_TOP
                , STR_MARGIN_LEFT
                , STR_DISPLAY
                , STR_BACKGROUND_COLOR
                , STR_HEIGHT
                , STR_NONE
                , STR_BLOCK
                , STR_FLEX
                , STR_POSITION
                , STR_ABSOLUTE
                , STR_TRANSPARENT
                , STR_BOX_SHADOW
                , STR_WIDTH
                , STR_TITLE
                , STR_BREAK
                , STR_CONTINUE
                , STR_PASS
                , STR_ONE_SPACE
                , STR_ONE_INDENT 
                , STR_MSG_BLOCK_DEPTH_MUSH_NOT_EXCEED_6
                , STR_CLICK
    
                , VP_BLOCK
                , VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF
                , VP_CLASS_PREFIX
    
                , VP_CLASS_APIBLOCK_BOARD
                , VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW
                , VP_CLASS_BLOCK_BOTTOM_HOLDER
                , VP_CLASS_BLOCK_SHADOWBLOCK_CONTAINER
                , VP_CLASS_APIBLOCK_BLOCK_HEADER
                , VP_CLASS_SELECTED_SHADOWBLOCK
    
                , VP_CLASS_STYLE_FLEX_ROW_BETWEEN
                , VP_CLASS_STYLE_FLEX_ROW_END
                , VP_CLASS_BLOCK_SUB_BTN_CONTAINER
    
                , STR_CHANGE_KEYUP_PASTE
    
                , STATE_className
                , STATE_defName
                , STATE_isIfElse
    
                , STATE_forBlockOptionType
                , STATE_isFinally
                , STATE_codeLine
    
                , COLOR_CLASS_DEF
                , COLOR_CONTROL
                , COLOR_CODE
    
                , COLOR_CLASS_DEF_STRONG
                , COLOR_CONTROL_STRONG
                , COLOR_CODE_STRONG
            
                , COLOR_WHITE
                , COLOR_LINENUMBER
    
                , ERROR_AB0002_INFINITE_LOOP } = constData;

    var Block = function(blockContainerThis, type , blockData) {
        var blockCodeLineType = type;
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS ) {
            var classNum = blockContainerThis.getClassNum();
            blockContainerThis.addClassNum();
        }
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
            var defNum = blockContainerThis.getDefNum();
            blockContainerThis.addDefNum();
        }
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.FOR ) {
            var forNum = blockContainerThis.getForNum();
            blockContainerThis.addForNum();
        }

        this.state = {
            type
            , blockType: BLOCK_TYPE.BLOCK
            , blockName: STR_NULL
            , opacity: 1
            
            , isLowerDepthChild: false
            , isRootBlock: false
            
            , isClicked: false
            , isCtrlPressed: false
            , isMoved: false
            , isNowMoved: false
            , isNodeBlockDoubleClicked: false

            , uuid: vpCommon.getUUID()
            , direction: BLOCK_DIRECTION.ROOT
            , depth: 0
            , tempBlockLeftHolderHeight: 0
            , blockNumber: 0
            , width: 0
            , blockHeaderWidth: 0
            , blockCodeLineWidth: 0
            , variableIndex: 0

            , codeLine: STR_NULL
            , nextBlockUUIDList: []
            , optionState: {
               
                className: `vpClass${classNum}`
                , parentClassName: STR_NULL

                , classInParamList: [STR_NULL]
              
                , defName: `vpFunc${defNum}`
                , defInParamList: []
                , defReturnType: DEF_BLOCK_ARG4_TYPE.NONE

                , ifConditionList: [
                     {
                        arg1: STR_NULL
                        , arg2: STR_NULL
                        , arg3: STR_NULL
                        , arg4: STR_NULL
                        , arg5: STR_NULL
                        , arg6: STR_NULL
                        , codeLine: STR_NULL
                        , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                ]
                , elifList: []
              
                , elifConditionList: [
                    {
                        arg1: STR_NULL
                        , arg2: STR_NULL
                        , arg3: STR_NULL
                        , arg4: STR_NULL
                        , arg5: STR_NULL
                        , arg6: STR_NULL
                        , codeLine: STR_NULL
                        , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                ]
             
                , isIfElse: false
        
                , forParam: {
                    arg1: STR_NULL
                    , arg2: STR_NULL
                    , arg3: FOR_BLOCK_ARG3_TYPE.INPUT_STR
                    , arg4: STR_NULL
                    , arg5: STR_NULL
                    , arg6: STR_NULL
                    , arg7: STR_NULL

                    , arg3InputStr: STR_NULL
                    , arg3Default: STR_NULL
                }
                , forBlockOptionType: 'for'
      
                , listforReturnVar: STR_NULL
                , listforPrevExpression: STR_NULL
                , listforConditionList: [
                    {  
                        arg1: STR_NULL
                        , arg2: STR_NULL
                        , arg3: FOR_BLOCK_ARG3_TYPE.INPUT_STR
                        , arg4: STR_NULL
                        , arg5: STR_NULL
                        , arg6: STR_NULL
                        , arg7: STR_NULL
       
                        , arg10: 'none'
                        , arg11: STR_NULL
                        , arg12: STR_NULL
                        , arg13: STR_NULL
                        , arg14: STR_NULL
                        , arg15: STR_NULL

                        , arg3InputStr: STR_NULL
                        , arg3Default: STR_NULL

                        , arg10InputStr: STR_NULL
                    }
                ]
                
                , whileCodeLine: 'False'
                , whileArgs: {
                    arg1: STR_NULL
                    , arg2: 'none'
                    , arg3: STR_NULL
                    , arg4: STR_NULL
                    , arg5: STR_NULL
                    , arg6: STR_NULL
                    , arg7: STR_NULL
                }
                , whileConditionList: [
                    {
                        arg1: STR_NULL
                        , arg2: STR_NULL
                        , arg3: STR_NULL
                        , arg4: STR_NULL
                        , arg5: STR_NULL
                        , arg6: STR_NULL
                        // , codeLine: ''
                        // , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                ]

                , exceptList: []
                , exceptConditionList: [
                    {
                        arg1: STR_NULL
                        , arg2: `none`
                        , arg3: STR_NULL
                        , codeLine: STR_NULL
                        , conditionType: IF_BLOCK_CONDITION_TYPE.ARG
                    }
                ]
                , finally: {
                    isFinally: false
                }
         
                ,baseImportList: [
                    baseImportNumpy = {
                        isImport: false
                        , baseImportName: 'numpy' 
                        , baseAcronyms: 'np' 
                    }   
                    , baseImportPandas = {
                        isImport: false
                        , baseImportName: 'pandas' 
                        , baseAcronyms: 'pd' 
                    }
                    , baseImportMatplotlib = {
                        isImport: false
                        , baseImportName: 'matplotlib.pyplot' 
                        , baseAcronyms: 'plt' 
                    }
                    , baseImportSeaborn = {
                        isImport: false
                        , baseImportName: 'seaborn' 
                        , baseAcronyms: 'sns' 
                    }
                    , baseImportOs = {
                        isImport: false
                        , baseImportName: 'os' 
                        , baseAcronyms: 'os' 
                    }
                    , baseImportSys = {
                        isImport: false
                        , baseImportName: 'sys' 
                        , baseAcronyms: 'sys' 
                    }
                    , baseImportTime = {
                        isImport: false
                        , baseImportName: 'time' 
                        , baseAcronyms: 'time' 
                    }
                    , baseImportDatetime = {
                        isImport: false
                        , baseImportName: 'datetime' 
                        , baseAcronyms: 'datetime' 
                    }
                    , baseImportRandom = {
                        isImport: false
                        , baseImportName: 'random' 
                        , baseAcronyms: 'random' 
                    }
                    , baseImportMath = {
                        isImport: false
                        , baseImportName: 'math' 
                        , baseAcronyms: 'math' 
                    }
                ]
                , customImportList: []
                , isBaseImportPage: true
              
                , lambdaArg1: STR_NULL
                , lambdaArg2List: [ ]
                , lambdaArg2m_List: [ ]
                , lambdaArg3: STR_NULL
                , lambdaArg4List: [ ]
          
                , returnOutParamList: [ ]
            
                , customCodeLine: STR_NULL
            }
        }

        this.nextBlockList = [];
        this.blockContainerThis = blockContainerThis;

        /** dom */
        this.rootDom = null;
        this.rootInnerDom = null;
        this.rootHeaderDom = null;
        this.containerDom = null;
        this.blockLeftHolderDom = null;
        this.blockNumInfoDom = null;
        this.depthInfoDom = null;
        this.blockLineNumberInfoDom = null;
        this.blockOptionPageDom = null;

        /** block */
        this.prevBlock = null;
        this.firstIndentBlock = null;
        this.holderBlock = null;
        this.childBlock_down = null;
        this.childBlock_indent = null;

        /** block`s type */
        this.ifElseBlock = null;
        this.finallyBlock = null;
        this.lastElifBlock = null;
        this.lastChildBlock = null;
        this.propertyBlockFromDef = null;

        /** api list block */
        this.funcID = null;
        this.optionPageLoadCallback = null;
        this.loadOption = null;
        this.importPakage = null;

        /** node block */
        this.isNodeBlockInput = false;

        var name = MapTypeToName(type);
        this.setBlockName(name);
    
        var blockCodeLineType = this.getBlockCodeLineType();

        if (blockData) {
            this.state.optionState = blockData.blockOptionState;
            this.state.uuid = blockData.UUID;
        } 
        if (blockData == undefined) {
            /** class block일 경우 */
            if (blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS) {
                var defBlock = this.blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.DEF);
                defBlock.setState({
                    defName: '__init__'
                });
                defBlock.init();
                var defBlockMainDom = defBlock.getBlockMainDom();
                RenderHTMLDomColor(defBlock, defBlockMainDom);

                var holderBlock = this.blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.HOLDER );
                this.setFirstIndentBlock(defBlock);

                this.setHolderBlock(holderBlock);
                holderBlock.setSupportingBlock(this);
                $(holderBlock.getBlockMainDom()).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);

                this.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
                this.appendBlock(defBlock, BLOCK_DIRECTION.INDENT);

                $(this.getHolderBlock().getBlockMainDom()).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF);

            /** def block일 경우 */
            } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
                
                var returnBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.RETURN );
                var holderBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.HOLDER );
                
                this.setHolderBlock(holderBlock);
                this.setFirstIndentBlock(returnBlock);
                holderBlock.setSupportingBlock(this);
                $(holderBlock.getBlockMainDom()).addClass(VP_BLOCK_BLOCKCODELINETYPE_CLASS_DEF);
                this.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
                this.appendBlock(returnBlock, BLOCK_DIRECTION.INDENT);

                $(this.getHolderBlock().getBlockMainDom()).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF);

            /** if, for, while, try block일 경우 */
            } else if ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.WHILE 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT 
                        || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY ) {

                var passBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.PASS);
                var holderBlock = this.blockContainerThis.createBlock( BLOCK_CODELINE_TYPE.HOLDER );
                
                this.setHolderBlock(holderBlock);
                this.setFirstIndentBlock(passBlock);
                holderBlock.setSupportingBlock(this);

                this.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
                this.appendBlock(passBlock, BLOCK_DIRECTION.INDENT);
            } 
        }
        
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.BREAK) {
            this.setState({
                customCodeLine: STR_BREAK
            });

        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.CONTINUE) {
            this.setState({
                customCodeLine: STR_CONTINUE
            });

        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.PASS) {
            this.setState({
                customCodeLine: STR_PASS
            });

        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.NODE) {
            this.blockContainerThis.addNodeBlock(this);
        }

        this.blockContainerThis.addBlock(this);

        this.init();
        this.renderMyColor(true);
    }

    Block.prototype.init = function() {
        var blockContainerThis = this.getBlockContainerThis();

        var blockMainDom = blockContainerThis.makeBlockDom(this, true);
        this.setBlockMainDom(blockMainDom);

        var blockDepthInfoDom = $(`<span class='vp-block-depth-info'></span>`);
        var isShowDepth = blockContainerThis.getIsShowDepth();
        if ( isShowDepth == false ) {
            $(blockDepthInfoDom).css(STR_OPACITY, 0);
        }
        this.setBlockDepthInfoDom(blockDepthInfoDom);
        $(blockMainDom).append(blockDepthInfoDom);

        var blockCodeLineType = this.getBlockCodeLineType();
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.HOLDER) {
            blockMainDom.classList.add(VP_CLASS_BLOCK_BOTTOM_HOLDER);
        } else if (blockCodeLineType != BLOCK_CODELINE_TYPE.HOLDER) {
            blockMainDom = blockContainerThis.makeBlockLineNumberInfoDom(this);
        }

        this.bindEventAll();

        if (blockCodeLineType == BLOCK_CODELINE_TYPE.TEXT) {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, STR_TRANSPARENT);
            $(blockMainDom).css(STR_WIDTH, NUM_TEXT_BLOCK_WIDTH);
        }
    }


    Block.prototype.writeCode = function(textInfo) {
        if (this.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE) {
            $(`#vp_apiblock_nodeblock_${this.getUUID()}`).html(textInfo);
        } else {
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BLOCK_HEADER + this.getUUID()).html(textInfo);
        }
    }

    // ** --------------------------- Block을 삭제, 수정, 불러오기 혹은 주변 block과의 관계를 규정하는 메소드들 --------------------------- */

    Block.prototype.getPrevBlock = function() {
        return this.prevBlock
    }
    Block.prototype.setPrevBlock = function(prevBlock) {
        this.prevBlock = prevBlock;
    }
    Block.prototype.addNextBlockList = function(nextBlock) {
        this.nextBlockList = [ ...this.nextBlockList, nextBlock]
    }
    Block.prototype.setNextBlockList = function(nextBlockList) {
        this.nextBlockList = nextBlockList;
    }
    Block.prototype.getNextBlockList = function() {
        return this.nextBlockList;
    }
    Block.prototype.setHolderBlock = function(holderBlock) {
        this.holderBlock = holderBlock;
    }
    Block.prototype.getHolderBlock = function() {
        return this.holderBlock;
    }

    Block.prototype.setChildBlock_down = function(childBlock_down) {
        this.childBlock_down = childBlock_down;
    }
    Block.prototype.getChildBlock_down = function() {
        return this.childBlock_down;
    }

    Block.prototype.setChildBlock_indent = function(childBlock_indent) {
        this.childBlock_indent = childBlock_indent;
    }
    Block.prototype.getChildBlock_indent = function() {
        return this.childBlock_indent;
    }

    Block.prototype.setSupportingBlock = function(supportingBlock) {
        this.supportingBlock = supportingBlock;
    }
    Block.prototype.getSupportingBlock = function() {
        return this.supportingBlock;
    }

    Block.prototype.setFirstIndentBlock = function(firstIndentBlock) {
        this.firstIndentBlock = firstIndentBlock;
    }
    Block.prototype.getFirstIndentBlock = function() {
        return this.firstIndentBlock;
    }


    Block.prototype.setPropertyBlockFromDef = function(propertyBlockFromDef) {
        this.propertyBlockFromDef = propertyBlockFromDef;
    }
    Block.prototype.getPropertyBlockFromDef = function() {
        return this.propertyBlockFromDef;
    }
    /**
     * if 블럭이 생성한 elifList 중에 가장 아래에 위치한 elif block을 set, get
     * @param {BLOCK} lastElifBlock 
     */
    Block.prototype.setLastElifBlock = function(lastElifBlock) {
        this.lastElifBlock = lastElifBlock;
    }
    Block.prototype.getLastElifBlock = function() {
        if (this.lastElifBlock) {
            return this.lastElifBlock;
        } else {
            return this;
        }
    }
    
    /**
     * @param { Block } lastChildBlock 
     */
    Block.prototype.setLastChildBlock = function(lastChildBlock) {
        this.lastChildBlock = lastChildBlock;
    }
    Block.prototype.getLastChildBlock = function() {
        return this.lastChildBlock;
    }

    Block.prototype.setIsNodeBlockInput = function(isNodeBlockInput) {
        this.isNodeBlockInput = isNodeBlockInput;
    }
    Block.prototype.getIsNodeBlockInput = function() {
        return this.isNodeBlockInput
    }

    /** 현재 root 블럭부터 모든 자식 블럭리스트 들을 전부 가져온다 */
    Block.prototype.getRootToChildBlockList = function() {
        var blockContainerThis = this.getBlockContainerThis();
        var rootBlock = blockContainerThis.getRootBlock()
        return rootBlock.getChildBlockList();
    }

    /** 현재 this 블럭부터 모든 자식 블럭리스트 들을 가져온다 */
    Block.prototype.getChildBlockList = function() {
        var nextBlockList = this.getNextBlockList();
        var stack = [];

        if (nextBlockList.length != 0) {
            stack.push(nextBlockList);
        }

        var childBlockList = [this];
        childBlockList = this._getChildBlockList(childBlockList, stack);
        return childBlockList;
    }

    /** 현재 root 블럭부터 하위 depth 자식 블럭리스트(동일 depth 블럭 제거) 들을 전부 가져온다 */
    Block.prototype.getRootToChildLowerDepthBlockList = function() {
        var blockContainerThis = this.getBlockContainerThis();
        var rootBlock = blockContainerThis.getRootBlock()
        return rootBlock.getChildLowerDepthBlockList();
    }

    /** 현재 this 블럭부터 하위 depth 자식 블럭리스트(동일 depth 블럭 제거) 들을 전부 가져온다 */
    Block.prototype.getChildLowerDepthBlockList = function() {
        var thisBlock = this;
        var nextBlockList = this.getNextBlockList();
        var stack = [];
        var childLowerDepthBlockList  = [];
        var lastChildBlock = null;
        var blockCodeLineType = this.getBlockCodeLineType();

        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.NODE ) {
            var current = null;
            var iteration = 0;
            stack = [this];
            while (stack.length != 0) {
                current = stack.shift();
                /** FIXME: 무한루프 체크 */
                if (iteration > NUM_MAX_ITERATION) {
                    console.log(ERROR_AB0002_INFINITE_LOOP);
                    break;
                }
                iteration++;

                /** 배열 일 때 */
                if (Array.isArray(current)) {
                    var currBlockList = current;
                    stack = DestructureFromBlockArray(stack, currBlockList);
                /** 배열 이 아닐 때 */
                } else {
                    var currBlock = current;
                    if ( (currBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE
                          || currBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT)
                        && currBlock.getUUID() != this.getUUID()) {
                        break;
                    }
                    childLowerDepthBlockList.push(currBlock);
                    this.setLastChildBlock(currBlock);
                    var nextBlockList = currBlock.getNextBlockList();
                    stack.unshift(nextBlockList);
                }
            }
            return childLowerDepthBlockList;
        } 

        /** indent 위치에 자식 블럭이 있는지 확인 
         *  indent 위치에 자식 블럭이 있어야 하위 depth 자식 블럭들을 가져올 수 있다.
        */
        if (nextBlockList.length != 0) {
            stack = this._pushFirstChildIndentBlock(stack, nextBlockList);
        }

        childLowerDepthBlockList  = [this];

        /** bottom holder block이 있으면 추가 */
        var holderBlock = null;
        if (IsCanHaveIndentBlock(blockCodeLineType)) {
            nextBlockList.some(block => {
                if (block.getDirection() == BLOCK_DIRECTION.DOWN) {
                    childLowerDepthBlockList.push(block);
                    lastChildBlock = holderBlock = block;
                    return true;
                }
            });
        } else {
            lastChildBlock = this;
        }
  
        if ( ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR
               || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY )
               && holderBlock != null) {

            var result = holderBlock.getElifBlockList(true);  
            var { elifList, 
                  lastChildBlock: _lastChildBlock } = result;
            if (_lastChildBlock !== null) {
                lastChildBlock = _lastChildBlock;
            }  
        
            childLowerDepthBlockList = this._getChildBlockList(childLowerDepthBlockList, stack);
            elifList.forEach(block => {
                childLowerDepthBlockList.push(block);
            });
            this.setLastChildBlock(lastChildBlock);
            return childLowerDepthBlockList;

        } else {
            this.setLastChildBlock(lastChildBlock);
            childLowerDepthBlockList = this._getChildBlockList(childLowerDepthBlockList, stack);
            return childLowerDepthBlockList;
        }
    }

    Block.prototype._pushFirstChildIndentBlock = function( stack, nextBlockList ) {
        var selectedBlock = null;
        nextBlockList.some(block => {
            if (block.getDirection() == BLOCK_DIRECTION.INDENT) {
                selectedBlock = block;
                stack.push(selectedBlock);
                return true;
            }
        });
        return stack;
    }

    /**
     * @private
     * @param {Array<Block>} travelBlockList 
     * @param {Array<Block>} stack 
     */
    Block.prototype._getChildBlockList = function(travelBlockList, stack) {
        var iteration = 0;
        var current;
        while (stack.length != 0) {
            current = stack.shift();
            /** FIXME: 무한루프 체크 */
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            iteration++;

            /** 배열 일 때 */
            if (Array.isArray(current)) {
                var currBlockList = current;
                stack = DestructureFromBlockArray(stack, currBlockList);
            /** 배열 이 아닐 때 */
            } else {
                var currBlock = current;
                travelBlockList.push(currBlock);
                var nextBlockList = currBlock.getNextBlockList();
                stack.unshift(nextBlockList);
            }
        }
        return travelBlockList;
    }
    
    /** 생성할 블럭이 6뎁스를 초과 할 경우 alert창을 띄워 막음 */
    Block.prototype.alertExceedDepth = function() {
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).find(VP_CLASS_PREFIX + VP_BLOCK).remove();
        vpCommon.renderAlertModal(STR_MSG_BLOCK_DEPTH_MUSH_NOT_EXCEED_6);
        this.resetOptionPage();
    }

    /** param으로 받아온 block을 this블럭의 자식으로 append. 
     *  FIXME: 대대적인 변경 필요
     *  @param {BLOCK} appendedBlock
     *  @param {BLOCK_DIRECTION} direction
     */
    Block.prototype.appendBlock = function(appendedBlock, direction) {
        var thisBlock = this;
        /**
         * depth가 6초과할 경우 alert
         */
        var depth = thisBlock.calculateDepthAndGet();
        if ( (depth >= NUM_EXCEED_DEPTH && direction == BLOCK_DIRECTION.INDENT)
            || depth > NUM_EXCEED_DEPTH) {
            appendedBlock.alertExceedDepth();
            return;
        }

        /** append할 block의 prev 블럭이 this 블럭일 때
         * 이동한 block을 내 위치에 다시 놓을 경우 
         * */
        var prevBlock = appendedBlock.getPrevBlock();
        if ( prevBlock ) {
            if (prevBlock.getUUID() == thisBlock.getUUID()) {
                return;
            }
        }
    
        thisBlock._deleteNextBlockFromPrevBlock(appendedBlock);

        appendedBlock.getChildLowerDepthBlockList();
        var lastChildBlock = appendedBlock.getLastChildBlock();

        // 새로 들어온 block의 이전 블럭을 현재 this블럭으로 정함
        appendedBlock.setPrevBlock(thisBlock);
        var nextBlockList = thisBlock.getNextBlockList();

        // append할 block의 direction이 down;
        if (direction == BLOCK_DIRECTION.DOWN) {
            if (appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.ELIF
                || appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.EXCEPT
                || appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.ELSE
                || appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.FOR_ELSE
                || appendedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.FINALLY ) {
                if (nextBlockList.length != 0) {
                    var getChildBlockList = appendedBlock.getChildBlockList();
                    getChildBlockList[getChildBlockList.length - 1].setNextBlockList([...nextBlockList]);
                }
                nextBlockList.forEach(block => {
                    block.setPrevBlock(getChildBlockList[getChildBlockList.length - 1]);
                    return true;          
                });
                this.setNextBlockList([appendedBlock]);  
            
            } else {
                thisBlock._nextLastChildBlockSetPrevBlock(prevBlock, appendedBlock.getDirection(), lastChildBlock);
                var holderBlock = appendedBlock.getHolderBlock();
                var lastChildBlock_downBlock;
                if(holderBlock){
                    lastChildBlock_downBlock = holderBlock;
                } else {
                    lastChildBlock_downBlock = lastChildBlock;
                }
                if (nextBlockList.length != 0) {
                    lastChildBlock_downBlock.setNextBlockList([...nextBlockList]);
                    nextBlockList.forEach(block => {
                        block.setPrevBlock(lastChildBlock_downBlock);
                        return true;          
                    });
                }
                thisBlock.setNextBlockList([appendedBlock]);  
                thisBlock.setChildBlock_down(appendedBlock);
            } 
        // append할 block의 direction이 indent;
        } else {
            thisBlock._nextLastChildBlockSetPrevBlock(prevBlock, appendedBlock.getDirection(), lastChildBlock);
            nextBlockList.some((nextBlock, index ) => {
                if (nextBlock.getDirection() == direction) {
                    // 새로 들어온 block이 기존에 자리잡고 있던 블록을 자식으로 append
                    nextBlock.setDirection(BLOCK_DIRECTION.DOWN);
                    lastChildBlock.addNextBlockList(nextBlock);
                    nextBlock.setPrevBlock(lastChildBlock);
                    nextBlockList.splice(index, 1);
                    return true;
                }
            });
            thisBlock.addNextBlockList(appendedBlock);
            thisBlock.setChildBlock_indent(appendedBlock);
        }
        
        appendedBlock.setDirection(direction);
    }

    Block.prototype._nextLastChildBlockSetPrevBlock = function(prevBlock, direction, lastChildBlock) {
        var nextLastChildBlock = null;
        if (lastChildBlock != null) {
            lastChildBlock.getNextBlockList().some( (block,index) => {
                if ( block.getDirection() == BLOCK_DIRECTION.DOWN) {
                    nextLastChildBlock = block;
                    nextLastChildBlock.setDirection(direction);

                    if (prevBlock != null) {
                        nextLastChildBlock.setPrevBlock(prevBlock);
                        prevBlock.addNextBlockList(nextLastChildBlock);
                    } else {
                        nextLastChildBlock.setPrevBlock(null);
                    }
            
                    lastChildBlock.getNextBlockList().splice(index, 1);
                    return true;
                }
            });
        }
    }

    /**
     * 하위 depth block들을 지운다
     */
    Block.prototype.deleteLowerDepthChildBlocks = function() {
        var blockContainerThis = this.getBlockContainerThis();
        /**
         *  만약 root 블럭일 경우 
         */
        if ( this.getPrevBlock() == null) {
            this.setDirection(BLOCK_DIRECTION.NONE);
            this.removeRootBlock();
            if (blockContainerThis.getBlockList().length == 0) {
                blockContainerThis.deleteContainerDom();
            };

        /**
         *  만약 root이 아닌 일반 블럭일 경우 
         */
        } else {
            this._deleteNextBlockFromPrevBlock();
            var prevBlock = this.getPrevBlock();
            var deletedBlockDirection = this.getDirection();
            var lastChildBlock = this.getLastChildBlock();
            this._nextLastChildBlockSetPrevBlock(prevBlock, deletedBlockDirection, lastChildBlock);
        }
        this.deleteBlockListDomAndData();
        blockContainerThis.reRenderAllBlock_asc();
    }
    
    Block.prototype._deleteNextBlockFromPrevBlock = function(thatBlock) {
        var prevBlock = this.getPrevBlock();
        var block = this;
        
        if ( thatBlock ) {
            prevBlock =  thatBlock.getPrevBlock();
            block = thatBlock;
        }

        if ( prevBlock ) {
            var nextBlockList = prevBlock.getNextBlockList();
            nextBlockList.some(( nextBlockBlock, index) => {
                if (nextBlockBlock.getUUID() == block.getUUID()) {
                    nextBlockList.splice(index, 1)
                    return true;
                }
            });
        }
    }
    /** 자식 블럭 리스트들 모두 제거 */
    Block.prototype.deleteBlock = function() {
        this._deleteNextBlockFromPrevBlock();

        var thisNextBlockDataList = this.getNextBlockList();
        var stack = [];
        if (thisNextBlockDataList.length != 0) {
            stack.push(thisNextBlockDataList);
        }

        var iteration = 0;
        var current;
        while (stack.length != 0) {
            /** FIXME: 무한루프 체크 */
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            iteration++;
            current = stack.pop();
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                current.forEach(block => {
                    stack.push(block);
                });
            /** 배열이 아닐 때 */
            } else {
                current.deleteBlock();
            }
        }

        this._deleteBlockDomAndData();
    }
    /** 
     *  blockContainer의 blockList에서 block 삭제
     */
    Block.prototype._deleteBlockDomAndData = function() {
        const blockMainDom = this.getBlockMainDom();
        $(blockMainDom).remove();
        $(blockMainDom).empty();

        /** blockContainer에서 block 데이터 삭제 제거 */
        const blockContainerThis = this.getBlockContainerThis();
        const blockUUID = this.getUUID(); 
        blockContainerThis.deleteBlock(blockUUID);
        blockContainerThis.deleteNodeBlock(blockUUID);
    }

    Block.prototype.deleteBlockListDomAndData = function() {
        this._deleteBlockDomAndData();
        var childLowerDepthBlockList = this.getChildLowerDepthBlockList();
        childLowerDepthBlockList.forEach(block => {
            block._deleteBlockDomAndData();
        });
    }
    // ** --------------------------- Block dom 관련 메소드들 --------------------------- */

    Block.prototype.getBlockMainDom = function() {
        return this.rootDom;
    }
    Block.prototype.setBlockMainDom = function(rootDom) {
        this.rootDom = rootDom;
    }

    Block.prototype.getBlockInnerDom = function() {
        return this.rootInnerDom;
    }
    Block.prototype.setBlockInnerDom = function(rootInnerDom) {
        this.rootInnerDom = rootInnerDom;
    }

    Block.prototype.getBlockHeaderDom = function() {
        return this.rootHeaderDom;
    }
    Block.prototype.setBlockHeaderDom = function(rootHeaderDom) {
        this.rootHeaderDom = rootHeaderDom;
    }

    Block.prototype.setBlockLeftHolderDom = function(blockLeftHolderDom) {
        this.blockLeftHolderDom = blockLeftHolderDom;
    }
    Block.prototype.getBlockLeftHolderDom = function() {
        return this.blockLeftHolderDom;
    }

    Block.prototype.setBlockDepthInfoDom = function(depthInfoDom) {
        this.depthInfoDom = depthInfoDom;
    }
    Block.prototype.getBlockDepthInfoDom = function() {
        return this.depthInfoDom;
    }

    Block.prototype.setBlockLineNumberInfoDom = function(blockLineNumberInfoDom) {
        this.blockLineNumberInfoDom = blockLineNumberInfoDom;
    }
    Block.prototype.getBlockLineNumberInfoDom = function() {
        return this.blockLineNumberInfoDom;
    }
 
    Block.prototype.renderRemoveDom = function(blockOldMainDom, moveChildListDom) {

        $(blockOldMainDom).remove();
            
        $(moveChildListDom).remove();
        $(moveChildListDom).empty();
    }

    Block.prototype.makeShadowDomList = function( shadowBlock, direction) {
        var thisBlock = this;
        var blockContainerThis = this.getBlockContainerThis();

        var indentPxNum = thisBlock.getIndentNumber();
        if (direction == BLOCK_DIRECTION.INDENT) {
            indentPxNum += NUM_INDENT_DEPTH_PX;
        }

        var shadowDom = shadowBlock.getBlockMainDom();
        $(shadowDom).css(STR_MARGIN_LEFT, indentPxNum + STR_PX);
        $(shadowDom).css(STR_DISPLAY,STR_BLOCK);
        $(shadowDom).addClass(VP_CLASS_SELECTED_SHADOWBLOCK);
        shadowBlock.setSelectBlock(this);

        var containerDom = blockContainerThis.getBlockContainerDom();
        containerDom.insertBefore(shadowDom, thisBlock.getBlockMainDom().nextSibling);
    }

    /** 현재 root 블럭부터 하위 depth 자식 블럭리스트(동일 depth 블럭 제거) 들을 전부 가져오고,
     *  가져온 block들의 정보를 가지고 html dom을 만들어 return 한다. 
     */
    Block.prototype.makeChildLowerDepthBlockDomList = function(isShadowBlock) {
        var blockContainerThis = this.getBlockContainerThis();
        var childBlockDomList = [];
        var rootDepth = 0;
        var $boardPage = blockContainerThis.getBoardPage_$();
        var $blockMainDom = null;
        var $moveChildListDom = null;

        var childBlockList = this.getChildLowerDepthBlockList();
        childBlockList.forEach((block, index) => {
            if (index == 0) {
                var depth = block.calculateDepthAndGet();
                rootDepth = depth;
                if (isShadowBlock == true) {
                    return;
                }
                var blockMainDom = blockContainerThis.makeBlockDom(block);
                $blockMainDom = $(blockMainDom);

                // /** 이동하는 block에 자식 block의 dom을 생성해 append*/
                $moveChildListDom = $(`<div class='vp-block-stack'><div>`);
                $blockMainDom.append($moveChildListDom);

                $boardPage.append($blockMainDom);

                $blockMainDom.css(STR_POSITION, STR_ABSOLUTE);
                return;

            } else {
                var blockMainDom = blockContainerThis.makeBlockDom(block);
                if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
                    $(blockMainDom).addClass(VP_CLASS_BLOCK_BOTTOM_HOLDER);
                    $(blockMainDom).css(STR_MARGIN_TOP, 0);
                    $(blockMainDom).css(STR_OPACITY, 10);
                }

                var depth = block.calculateDepthAndGet();
                var indentPxNum = block.getIndentNumber();
                indentPxNum -= rootDepth * NUM_INDENT_DEPTH_PX;
         
                $(blockMainDom).css(STR_MARGIN_LEFT, indentPxNum + STR_PX);
                childBlockDomList.push(blockMainDom);
            }
        });
        

        if (isShadowBlock == false) {
            var $frag = $(document.createDocumentFragment());
            childBlockDomList.forEach(childDom => {
                $frag.append(childDom);
            });
            $moveChildListDom.append($frag);
        }

        if (isShadowBlock === true) {
            return childBlockDomList;
        } else {
            return {
                $moveChildListDom, 
                $blockNewMainDom: $blockMainDom
            }
        }
    }

    /** block main dom의 width, height 값을 가져온다 */
    Block.prototype.getBlockMainDomPosition = function() {
        var blockMainDom = this.getBlockMainDom();
        var clientRect = $(blockMainDom)[0].getBoundingClientRect();
        return clientRect;
    }

    // ** --------------------------- Block 멤버변수의 set, get 관련 메소드들 --------------------------- */
    Block.prototype.setDepth = function(depth) {
        this.state.depth = depth;
    }

    Block.prototype.getDepth = function() {
        return this.state.depth;
    }

    Block.prototype.getBlockCodeLineType = function() {
        return this.state.type;
    }

    Block.prototype.getBlockName = function() {
        return this.state.blockName;
    }
    Block.prototype.setBlockName = function(blockName) {
        this.setState({
            blockName
        });
    }
    Block.prototype.getUUID = function() {
        return this.state.uuid;
    }
    Block.prototype.setUUID = function(uuid) {
        // this.state.uuid = uuid;
        this.setState({
            uuid
        });
    }
    /**
     * @param {ENUM} direction INDENT OR DOWN
     */
    Block.prototype.setDirection = function(direction) {
        this.setState({
            direction
        })
    }
    Block.prototype.getDirection = function() {
        return this.state.direction;
    }

    Block.prototype.getNextBlockUUIDList = function() {
        return this.state.nextBlockUUIDList;
    }
    Block.prototype.setNextBlockUUIDList = function(nextBlockUUIDList) {
        this.setState({
            nextBlockUUIDList
        });
    }

    Block.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }

    /**
     *  순간 순간 임시로 변하는 left holder height
     */
    Block.prototype.getTempBlockLeftHolderHeight = function() {
        return this.state.tempBlockLeftHolderHeight;
    }
    
    Block.prototype.setTempBlockLeftHolderHeight = function(tempBlockLeftHolderHeight) {
        this.setState({
            tempBlockLeftHolderHeight
        });
    }

    Block.prototype.setIsClicked = function(isClicked) {
        this.setState({
            isClicked
        });
    }

    Block.prototype.getIsClicked = function() {
        return this.state.isClicked;
    }

    Block.prototype.getIsCtrlPressed = function() {
        return this.state.isCtrlPressed;
    }
    Block.prototype.setIsCtrlPressed = function(isCtrlPressed) {
        this.setState({
            isCtrlPressed
        });
    }

    Block.prototype.getIsMoved = function() {
        return this.state.isMoved;
    }
    Block.prototype.setIsMoved = function(isMoved) {
        this.setState({
            isMoved
        });
    }

    Block.prototype.getIsNowMoved = function() {
        return this.state.isNowMoved;
    }
    Block.prototype.setIsNowMoved = function(isNowMoved) {
        this.setState({
            isNowMoved
        });
    }

    /**
     * 코드를 생성하기위해 IndentString을 가져오는 함수
     * depth 1개 당 TAB 1개
     * @param {number} rootDepth  기본값 0
     */
    Block.prototype.getIndentString = function(rootDepth = 0) {
        var depth = this.getDepth() - rootDepth;
        var indentString = STR_NULL;
        while (depth-- != 0) {
            indentString += STR_ONE_INDENT;
        }
        return indentString;
    }

    /**
     * 코드를 생성하기위해 IndentNumber을 가져오는 함수
     */
    Block.prototype.getIndentNumber = function() {
        var depth = this.getDepth();
        var indentPxNum = 0;
        while (depth-- != 0) {
            indentPxNum += NUM_INDENT_DEPTH_PX;
        }
        return indentPxNum;
    }

    Block.prototype.getIsNodeBlockToggled = function() {
        return this.state.isNodeBlockDoubleClicked;
    }
    Block.prototype.setIsNodeBlockToggled = function(isNodeBlockDoubleClicked) {
        this.state.isNodeBlockDoubleClicked = isNodeBlockDoubleClicked;
    }

    /**  variableIndex을 set, get, add 
     */
    Block.prototype.setVariableIndex = function(variableIndex) {
        this.setState({
            variableIndex
        });
    }

    Block.prototype.getVariableIndex = function() {
        return this.state.variableIndex;
    }

    Block.prototype.addVariableIndex = function() {
        this.state.variableIndex++
        return this.state.variableIndex;
    }

    /** code를 생성하는 메소드 */
    Block.prototype.setCodeLineAndGet = function(indentString = STR_NULL, isRun = false) {
        var thisBlock = this;
        var codeLine = STR_NULL;
        var blockName = this.getBlockName();

        if (indentString == undefined) {
            indentString = '';
        } 

        codeLine += indentString;

        var type = thisBlock.getBlockCodeLineType();
        switch (type) {
            case BLOCK_CODELINE_TYPE.NODE: {
                codeLine += `# [Visual Python] Node ${thisBlock.getBlockNumber()} : ${thisBlock.getState(STATE_codeLine)}`;
                break;
            }
            case BLOCK_CODELINE_TYPE.API: {
                // console.log('API');
                vpCommon.setIsAPIListRunCode(isRun);
                var apicode = MapNewLineStrToIndentString( thisBlock.getImportPakage().generateCode(false, false), 
                                                       indentString);
 
                thisBlock.getImportPakage().metaSave();   
                thisBlock.getImportPakage().metaGenerate(); 

                if (apicode.indexOf('BREAK_RUN') != -1) {
                    // console.log('BREAK_RUN');
                    return 'BREAK_RUN';
                } else {
                    codeLine += apicode;
                }

                break;
            }
            //class
            case BLOCK_CODELINE_TYPE.CLASS: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += thisBlock.getState(STATE_className);
                codeLine += GenerateClassInParamList(thisBlock);

                break;
            }
            //def
            case BLOCK_CODELINE_TYPE.DEF: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += thisBlock.getState(STATE_defName);
                codeLine += GenerateDefInParamList(thisBlock);
            
                break;
            }
            //if
            case BLOCK_CODELINE_TYPE.IF: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += GenerateIfConditionList(thisBlock, BLOCK_CODELINE_TYPE.IF);
                codeLine += `:`;
                break;
            }
            //for
            case BLOCK_CODELINE_TYPE.FOR: {
                var forBlockOptionType = thisBlock.getState(STATE_forBlockOptionType);
                if (forBlockOptionType == FOR_BLOCK_TYPE.FOR) {
                    codeLine += `${blockName.toLowerCase()}`;
                    codeLine += STR_ONE_SPACE;
                    codeLine += GenerateForParam(thisBlock);
                    codeLine += `:`;
                } else {
                    codeLine += GenerateListforConditionList(thisBlock);
                }
             
                break;
            }
            //while
            case BLOCK_CODELINE_TYPE.WHILE: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine +=  GenerateWhileConditionList(thisBlock);
                codeLine += `:`;
                break;
            }
            /** import */
            case BLOCK_CODELINE_TYPE.IMPORT: {
                codeLine += GenerateImportList(thisBlock, indentString);
                break;
            }
            /** api */
            case BLOCK_CODELINE_TYPE.API: {
                break;
            }
            /** try */
            case BLOCK_CODELINE_TYPE.TRY: {
                codeLine += `${blockName.toLowerCase()}:`;
                break;
            }
            /** return */
            case BLOCK_CODELINE_TYPE.RETURN: {
                codeLine += `${blockName.toLowerCase()} `;
                codeLine += GenerateReturnOutParamList(thisBlock);

                break;
            }

            /** break */
            case BLOCK_CODELINE_TYPE.BREAK: {
                codeLine += MapNewLineStrToIndentString(thisBlock.getState(STATE_codeLine), indentString);
                break;
            }
            /** continue */
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                codeLine += MapNewLineStrToIndentString(thisBlock.getState(STATE_codeLine), indentString);
                break;
            }
            /** pass */
            case BLOCK_CODELINE_TYPE.PASS: {
                codeLine += MapNewLineStrToIndentString(thisBlock.getState(STATE_codeLine), indentString);
                break;
            }
   
            /** elif */
            case BLOCK_CODELINE_TYPE.ELIF: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += GenerateIfConditionList(thisBlock,  BLOCK_CODELINE_TYPE.ELIF);
                codeLine += `:`;
                break;
            }
            /** else */
            case BLOCK_CODELINE_TYPE.ELSE: {
                codeLine += `${blockName.toLowerCase()}:`;
                break;
            }
            /** for else */
            case BLOCK_CODELINE_TYPE.FOR_ELSE: {
                codeLine += `${blockName.toLowerCase()}:`;
                break;
            }
            /** except */
            case BLOCK_CODELINE_TYPE.EXCEPT: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += STR_ONE_SPACE;
                codeLine += GenerateExceptConditionList(thisBlock);
                codeLine += `:`;
                break;
            }
            /** finally */
            case BLOCK_CODELINE_TYPE.FINALLY: {
                codeLine += `${blockName.toLowerCase()}:`;
                break;
            }
            /** code */
            case BLOCK_CODELINE_TYPE.CODE: {
                codeLine += MapNewLineStrToIndentString(thisBlock.getState(STATE_codeLine), indentString);
                break;
            }
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                codeLine += '@';
                codeLine += MapNewLineStrToIndentString(thisBlock.getState(STATE_codeLine), indentString);
                break;
            }
            case BLOCK_CODELINE_TYPE.LAMBDA: {
                codeLine += GenerateLambdaParamList(thisBlock);
                break;
            }
            case BLOCK_CODELINE_TYPE.COMMENT: {
                codeLine += '#';
                codeLine += thisBlock.getState(STATE_codeLine).replace(/(\r\n\t|\n|\r\t)/gm,"\n#");
                break;
            }
            case BLOCK_CODELINE_TYPE.PRINT: {
                codeLine += `${blockName.toLowerCase()}`;
                codeLine += `(`;
                codeLine += thisBlock.getState(STATE_codeLine).replace(/(\r\n\t|\n|\r\t)/gm,",");
                codeLine += `)`;
                break;
            }
        }
        this.state.codeLine = codeLine;
        return codeLine;
    }

    Block.prototype.getCodeLine = function() {
        return this.state.codeLine;
    }

    /**
     * block의 depth를 계산하고 depth 를 가져오는 함수
     */
    Block.prototype.calculateDepthAndGet = function() {
        var depth = 0;
        var currBlock = this;
        var direction = this.getDirection();

        var iteration = 0;
        var prevBlock = currBlock;
        while (prevBlock.getPrevBlock() != null) {
            prevBlock = prevBlock.getPrevBlock();
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            iteration++;
            
            if (direction == BLOCK_DIRECTION.INDENT
                && prevBlock.getDirection() != BLOCK_DIRECTION.DOWN ) {
                    depth++;
            } else {
                if (prevBlock.getDirection() == BLOCK_DIRECTION.INDENT) {
                    depth++;
                } 
            }
        }
        return depth;
    }

    /**
     * block의 left holder의 height를 계산하고 height를 set
     */
    Block.prototype.calculateLeftHolderHeightAndSet = function() {
        var blockCodeLineType = this.getBlockCodeLineType();
        var blockHeight = 0;
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
            blockHeight += NUM_BLOCK_BOTTOM_HOLDER_HEIGHT;
        }

        var childBlockList = this.getChildLowerDepthBlockList();
        childBlockList.forEach(childBlock => {
            if (childBlock == null) {
                return;
            }
            
            if ( childBlock.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER ) {
                blockHeight += NUM_BLOCK_HEIGHT_PX;
            } else {
                blockHeight += NUM_BLOCK_BOTTOM_HOLDER_HEIGHT;
            }
        });

        this.setTempBlockLeftHolderHeight(blockHeight);
    }

    /**
     * block의 width를 set, get
     */
    Block.prototype.getWidth = function() {
        return this.state.width;
    }
    Block.prototype.setWidth = function(width) {
        this.setState({
            width
        });
    }

    /**
     * block의 blockHeaderWidth를 set, get
     */
    Block.prototype.getBlockHeaderWidth = function() {
        return this.state.blockHeaderWidth;
    }
    Block.prototype.setBlockHeaderWidth = function(blockHeaderWidth) {
        this.setState({
            blockHeaderWidth
        });
    }

    /**
     * block의 blockCodeLineWidth를 set, get
     */
    Block.prototype.getBlockCodeLineWidth = function() {
        return this.state.blockCodeLineWidth;
    }
    Block.prototype.setBlockCodeLineWidth = function(blockCodeLineWidth) {
        this.setState({
            blockCodeLineWidth
        });
    }

    Block.prototype.setBlockNumber = function(blockNumber) {
        this.blockNumber = blockNumber;
    }
    Block.prototype.getBlockNumber = function() {
        return this.blockNumber;
    }

    Block.prototype.setMovedBlockListOpacity = function(opacityNum) {
        var str = STR_NULL;
        if (opacityNum == 0) {
            str = STR_NONE;
        } else {
            str = STR_BLOCK;
        }

        var childBlockList = this.getChildLowerDepthBlockList();
        childBlockList.forEach(block => {
            var blockMainDom = block.getBlockMainDom();
            $(blockMainDom).css(STR_OPACITY, opacityNum);
            $(blockMainDom).css(STR_DISPLAY, str);
        });
    }
    // ** --------------------------- Block render 관련 메소드들 --------------------------- */

    Block.prototype.renderBlockLeftHolderHeight = function(px) {
        $( this.getBlockLeftHolderDom() ).css(STR_HEIGHT, px + STR_PX);
    }
    Block.prototype.resetBlockLeftHolderHeight = function() {
        $( this.getBlockLeftHolderDom() ).css(STR_HEIGHT, NUM_DEFAULT_BLOCK_LEFT_HOLDER_HEIGHT + STR_PX);
    }

    /** */
    Block.prototype.renderMyColor = function(isColor) {
        if (this.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
            return;
        }

        /** block color 색칠 */
        this.renderSelectedMainBlockBorderColor(isColor);
        this.renderSelectedBlockColor(isColor);
        var childLowerDepthBlockList = this.getChildLowerDepthBlockList();
        childLowerDepthBlockList.forEach(block => {
            block.renderSelectedBlockColor(isColor);
        });
    }

    /**
     * block 클릭시 block border 노란색으로 변경
     */
    Block.prototype.renderSelectedMainBlockBorderColor = function(isColor) {
        var blockContainerThis = this.getBlockContainerThis();
        var blockList = blockContainerThis.getBlockList();
        blockList.forEach(block => {
            $(block.getBlockMainDom()).css(STR_BORDER, '1px solid transparent');
        });

        if (isColor == false) {
            return;
        }

        if (this.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
            $(this.getBlockMainDom()).css('border-left', '1px solid #F37704');
        } else {
            $(this.getBlockMainDom()).css(STR_BORDER, '1px solid #F37704');
        }
     
    }

    /**
     * block 클릭시 block border 주황.색으로 변경
     */
    Block.prototype.renderSelectedBlockColor = function(isReset) {
        var blockMainDom = this.getBlockMainDom();
        var blockCodeLineType = this.getBlockCodeLineType();
        if (blockCodeLineType == BLOCK_CODELINE_TYPE.HOLDER ) {
            return;
        } 
        if (isReset == true) {
            $(blockMainDom).css(STR_DISPLAY, STR_FLEX);
        }
        /** class & def 블럭 */
        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.CLASS 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.DEF) {
            
            if (isReset == true) {
                $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF_STRONG);
            } else {
                $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CLASS_DEF);
            }
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
            || blockCodeLineType == BLOCK_CODELINE_TYPE.LAMBDA
            || blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT 
            || blockCodeLineType == BLOCK_CODELINE_TYPE.PROPERTY   ) {
            if (isReset == true) {
                $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CONTROL_STRONG);
            } else {
                $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CONTROL);
            }
 
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.TEXT ) {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, STR_TRANSPARENT);
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK ) {
            $(blockMainDom).css(STR_BACKGROUND_COLOR, STR_TRANSPARENT);
        } else {
            if (isReset == true) {
                $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CODE_STRONG);
            } else {
                $(blockMainDom).css(STR_BACKGROUND_COLOR, COLOR_CODE);
            }
        } 
    }

    /** elif block list를 가져온다
     * @param {boolean} isChildLowerDepthBlock
     * @return {Array<Block>}
     */
    Block.prototype.getElifBlockList = function(isChildLowerDepthBlock) {
        var thisBlock = this;
        var lastChildBlock = null;

        var elifList = [];
        var nextBlockList = thisBlock.getNextBlockList();
        var stack = [];
        if (nextBlockList.length != 0) {
            stack.push(nextBlockList);
        }

        var isBreak = false;
        var current;
        while (stack.length != 0) {
            current = stack.shift();
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                current.forEach(block => {
                    var blockCodeLineType = block.getBlockCodeLineType();
                    var blockDirection = block.getDirection();
                    if ( blockDirection == BLOCK_DIRECTION.DOWN 
                        && ( blockCodeLineType == BLOCK_CODELINE_TYPE.IF
                            || blockCodeLineType == BLOCK_CODELINE_TYPE.TRY
                            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR )) {
                        isBreak = true;
                    }

                    if ( blockDirection == BLOCK_DIRECTION.DOWN ) {
                        stack.push(block);
                        if (isChildLowerDepthBlock === true) {
                            if ( blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY 
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT ) {
                        
                                lastChildBlock = block.getHolderBlock();
                                elifList.push(lastChildBlock);

                                var elifOrElseChildLowerDepthBlockList = block.getChildLowerDepthBlockList();
                                elifOrElseChildLowerDepthBlockList.forEach(elifOrElseChildLowerDepthBlock => {
                                    elifList.push(elifOrElseChildLowerDepthBlock);
                                });
                            }
                        } else {
                            if ( blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
                                || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT ) {
                                elifList.push(block);    
                            }
                        }
                    }
                });

            } else {
                var currBlock = current;
                var nextBlockList = currBlock.getNextBlockList();
                stack.unshift(nextBlockList);
            }

            if (isBreak) {
                break;
            }
        }
        if (isChildLowerDepthBlock === true) {
            return {
                elifList
                , lastChildBlock
            }
        } else {
            return elifList;
        }
    }

    Block.prototype.resetOptionPage = function() {
        var blockContainerThis = this.getBlockContainerThis();
        var blockUUID = this.getUUID();
        var blockCodeLineType = this.getBlockCodeLineType();
        var optionPageSelector = VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW;
        var blockOptionPageDom = InitElseBlockOption(this, optionPageSelector);
        blockContainerThis.setOptionDom(blockUUID, blockCodeLineType, blockOptionPageDom);   
        blockContainerThis.getOptionDomPool(blockOptionPageDom);
    }

    /**
     * Block Type에 맵핑되는 Option을 Option tab에 렌더링하는 html 함수
     * @param {boolean} isChild true면 옵션 페이지에 자식 옵션으로 표시됨
     */
    Block.prototype.renderOptionPage = function() {
        var thisBlock = this;
        if (thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
            return;
        }

        var optionPageSelector = VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW;
        var blockContainerThis = this.getBlockContainerThis();
        var blockUUID = this.getUUID();
        var blockOptionPageDom = blockContainerThis.getOptionDom(blockUUID);
    
        var blockCodeLineType = thisBlock.getBlockCodeLineType();
        switch(blockCodeLineType) {
            /** class */
            case BLOCK_CODELINE_TYPE.CLASS: {
                blockOptionPageDom = InitClassBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** def */
            case BLOCK_CODELINE_TYPE.DEF: {
                blockOptionPageDom = InitDefBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** if */
            case BLOCK_CODELINE_TYPE.IF: {
                blockOptionPageDom = InitIfBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** elif */
            case BLOCK_CODELINE_TYPE.ELIF: {
                blockOptionPageDom = InitElifBlockOption(thisBlock, optionPageSelector);
                break;
            }     
            /** else */
            case BLOCK_CODELINE_TYPE.ELSE: {
                blockOptionPageDom = InitElseBlockOption(thisBlock, optionPageSelector);
                break;
            }    

            /** for */
            case BLOCK_CODELINE_TYPE.FOR: {
                var forBlockOptionType = thisBlock.getState(STATE_forBlockOptionType);
                if (forBlockOptionType == FOR_BLOCK_TYPE.FOR) {
                    blockOptionPageDom = InitForBlockOption(thisBlock, optionPageSelector);
                } else {
                    blockOptionPageDom = InitListForBlockOption(thisBlock, optionPageSelector);
                }
                break;
            }
            /** while */
            case BLOCK_CODELINE_TYPE.WHILE: {
                blockOptionPageDom = InitWhileBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Try */
            case BLOCK_CODELINE_TYPE.TRY: {
                blockOptionPageDom = InitTryBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** Except */
            case BLOCK_CODELINE_TYPE.EXCEPT: {
                blockOptionPageDom = InitExceptBlockOption(thisBlock, optionPageSelector);
                break;
            }   
            /** Return */
            case BLOCK_CODELINE_TYPE.RETURN : {
                blockOptionPageDom = InitReturnBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Code block */
            case BLOCK_CODELINE_TYPE.CODE: {
                blockOptionPageDom = InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Break block */
            case BLOCK_CODELINE_TYPE.BREAK: {
                blockOptionPageDom = InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }
       
            /** Continue block */
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                blockOptionPageDom = InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }
          
            /** Property block */
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                blockOptionPageDom = InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** Pass block */
            case BLOCK_CODELINE_TYPE.PASS:  {
                blockOptionPageDom = InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Lambda block */
            case BLOCK_CODELINE_TYPE.LAMBDA: {
                blockOptionPageDom = InitLambdaBlockOption(thisBlock, optionPageSelector);
                break;
            }
            /** Comment block */
            case BLOCK_CODELINE_TYPE.COMMENT: {
                blockOptionPageDom = InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Sample block */
            case BLOCK_CODELINE_TYPE.SAMPLE: {
                blockOptionPageDom = InitSampleBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Print block */
            case BLOCK_CODELINE_TYPE.PRINT: {
                blockOptionPageDom = InitCodeBlockOption(thisBlock, optionPageSelector);
                break;
            }  

            /** Api block */
            case BLOCK_CODELINE_TYPE.API: {
                blockOptionPageDom = InitApiBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Import block */
            case BLOCK_CODELINE_TYPE.IMPORT: {
                blockOptionPageDom = InitImportBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Node block */
            case BLOCK_CODELINE_TYPE.NODE: {
                blockOptionPageDom = InitNodeBlockOption(thisBlock, optionPageSelector);
                break;
            }

            /** Text block */
            case BLOCK_CODELINE_TYPE.TEXT: {
                blockOptionPageDom = InitTextBlockOption(thisBlock, optionPageSelector);
                break;
            }
        }
        // console.log('blockOptionPageDom',blockOptionPageDom);
        blockContainerThis.setOptionDom(blockUUID, blockCodeLineType, blockOptionPageDom);   
        blockContainerThis.getOptionDomPool(blockOptionPageDom);
    }

    // ** --------------------------- Block state 관련 메소드들 --------------------------- */
    Block.prototype.setState = function(newState) {
        this.state = ChangeOldToNewState(this.state, newState);
        this.consoleState();
        this.setBlockTitle();
    }

    /**특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    Block.prototype.getState = function(stateKeyName) {
        return FindStateValue(this.state, stateKeyName);
    }
    Block.prototype.getStateAll = function() {
        return this.state;
    }
    Block.prototype.consoleState = function() {
        // console.log(this.state);
    }

    /** 변경된 codeline state를 html title로 set */
    Block.prototype.setBlockTitle = function() {
        var codeLine = this.getCodeLine();

        var blockMainDom = this.getBlockMainDom();
        $(blockMainDom).attr(STR_TITLE,  codeLine);
    }

    /** ---------------------------이벤트 함수 바인딩--------------------------- */
    Block.prototype.bindEventAll = function() {
        var blockCodeLineType = this.getBlockCodeLineType();

        if ( blockCodeLineType == BLOCK_CODELINE_TYPE.ELIF
            || blockCodeLineType == BLOCK_CODELINE_TYPE.ELSE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FOR_ELSE
            || blockCodeLineType == BLOCK_CODELINE_TYPE.EXCEPT
            || blockCodeLineType == BLOCK_CODELINE_TYPE.FINALLY ) {
            this.bindClickEvent();
            this.bindLineNumberEvent();
  
        } else {
            this.bindClickEvent();
            this.bindDragEvent();
            this.bindLineNumberEvent();
        }
    }
    
    Block.prototype.bindLineNumberEvent = function() {
        var thisBlock = this;
        var blockLineNumberInfoDom = this.getBlockLineNumberInfoDom();
        $(blockLineNumberInfoDom).off();

        if (this.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE) {
            $(blockLineNumberInfoDom).hover(function(event) {
                $(blockLineNumberInfoDom).html(`<div class='vp-apiblock-circle-play'></div>`);
                $(blockLineNumberInfoDom).css(STR_BACKGROUND_COLOR, COLOR_WHITE);
                event.preventDefault();
            }, function(event) {
                $(blockLineNumberInfoDom).text(thisBlock.getBlockNumber());
                $(blockLineNumberInfoDom).css(STR_BACKGROUND_COLOR, COLOR_LINENUMBER);
                event.preventDefault();
            });
        } else if (this.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
            $(blockLineNumberInfoDom).html(`<div class='vp-apiblock-circle-play'></div>`);
            $(blockLineNumberInfoDom).css(STR_BACKGROUND_COLOR, COLOR_WHITE);
        }

        $(blockLineNumberInfoDom).on(STR_CLICK, function(event) {
            thisBlock.runThisBlock();
            event.preventDefault();
            event.stopPropagation();
        });
    }
    
    /**
     * TODO: 추후 개선해야 할 메소드 
     * @async
     * block drag시 발생하는 이벤트 메소드 
     */
    Block.prototype.bindDragEvent = function() {
        var thisBlock = this;
        
        var blockContainerThis = this.getBlockContainerThis();
        var blockCodeLineType = this.getBlockCodeLineType();
        var blockOldMainDom = this.getBlockMainDom();
        var x = 0;
        var y = 0;
  
        var shadowBlock = null;
        var nowMovedBlockList = [];
        var selectedBlock = null;
        var selectedBlockDirection = null;

        var currCursorX = 0;
        var currCursorY = 0;

        /** 제이쿼리 변수 */
        var $blockNewMainDom = null;
        var $blockOldMainDom = $(blockOldMainDom);
   
        var $moveChildListDom = null;
        var $boardPage = blockContainerThis.getBoardPage_$();
        var $shadowBlockMainDom = null;
        
        var isOnlyRootBlockAtBoard = false;
        var isCollision50perInner = true;
        $blockOldMainDom.draggable({ 
            revert: 'invalid',
            revertDuration: 200,
            containment: VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD,
            cursor: 'move', 
            distance: 10,
            start: (event, ui) => {
               
                /** board 초록색 border 색칠 */
                blockContainerThis.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);

                ( { $blockNewMainDom, $moveChildListDom }  = thisBlock.makeChildLowerDepthBlockDomList(false));
                /** 이동하는 하위 depth Block 들 opacity 0 */
                thisBlock.setMovedBlockListOpacity(0);

                /** Node 블럭 toggle 중일 경우 이동시 자식 블럭 안보여줌 */
                if ( thisBlock.getIsNodeBlockToggled() == true) {
                    $moveChildListDom.css(STR_OPACITY,0);
                }

                /** shadow block 생성 */
                var shadowChildBlockDomList = thisBlock.makeChildLowerDepthBlockDomList(true);
                shadowBlock = blockContainerThis.makeShadowBlock( blockContainerThis, blockCodeLineType,
                                                                  shadowChildBlockDomList, thisBlock);

                blockContainerThis.reLoadBlockListLeftHolderHeight();

            },
            drag: async (event, ui) => {
                    /** 현재 drag하는 Block의 위치 구현 */
                    blockContainerThis.setCurrCursorY(event.clientY);
    
                    currCursorX = event.clientX; 
                    currCursorY = event.clientY; 
    
                    var scrollHeight =  blockContainerThis.getScrollHeight();
                    var maxWidth =  blockContainerThis.getMaxWidth();
 
                    /** 블럭 드래그시 
                     *  왼쪽 정렬  
                     */
                    x = currCursorX - $boardPage.offset().left;

                    var nodeBlockAdd = 0;
                    if (thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE
                        || thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
                        nodeBlockAdd += 20;
                    } 
                    y = currCursorY - ( $boardPage.offset().top - $boardPage.scrollTop() ) - nodeBlockAdd;
    
                    /** 이동한 블럭들의 루트블럭 x좌표가 editor 화면의 maxWidth 이상 일때 */
                    if (x > maxWidth - $blockNewMainDom.width()) {
                        x = maxWidth - $blockNewMainDom.width();
                    }
                    /** 이동한 블럭들의 루트블럭 y좌표가 editor 화면의 maxHeight 이상 일때 */
                    if (y > scrollHeight - ( $moveChildListDom.height() + NUM_BLOCK_HEIGHT_PX ) ) {
                        y = scrollHeight - ( $moveChildListDom.height() + NUM_BLOCK_HEIGHT_PX );
                    }
                    /** 이동한 블럭들의 루트블럭 y좌표가 0 이하 일때 */
                    if (y < 0) {
                        y = 0;
                    }
    
                    $blockNewMainDom.css(STR_TOP, y + STR_PX);
                    $blockNewMainDom.css(STR_LEFT, x + STR_PX);
                    ({ selectedBlock, selectedBlockDirection} = blockContainerThis.dragBlock(true, thisBlock, shadowBlock, 
                                                                    selectedBlock,selectedBlockDirection,currCursorX, currCursorY));
                 
                }, 
                stop: function(event, ui) { 
                    // console.log('stop start');
                    
                    // 화면 밖으로 나갔을 때, 재조정
                    var maxWidth =  blockContainerThis.getMaxWidth();
                    var maxHeight =  blockContainerThis.getMaxHeight();
    
                    var isDisappeared = false;
                    /** 이동한 블럭들의 루트블럭 x좌표가 0 이하 일때 */
                    if (x < 0) {
                        x = 0;
                        isDisappeared = true;
                    }
                    /** 이동한 블럭들의 루트블럭 x좌표가 editor 화면의 maxWidth 이상 일때 */
                    if (x > maxWidth - $blockOldMainDom.width()) {
                        x = maxWidth - $blockOldMainDom.width();
                        isDisappeared = true;
                    }
                    /** 이동한 블럭들의 루트블럭 y좌표가 editor 화면의 maxHeight 이상 일때 */
                    if (y > maxHeight - ( $moveChildListDom.height() + NUM_BLOCK_HEIGHT_PX ) ) {
                        y = maxHeight - ( $moveChildListDom.height() + NUM_BLOCK_HEIGHT_PX );
    
                    }
                    /** 이동한 블럭들의 루트블럭 y좌표가 0 이하 일때 */
                    if (y < 0) {
                        y = 0;
                        isDisappeared = true;
                    }
    
                    selectedBlock = shadowBlock.getSelectBlock();
                    
                    /** 블록이 화면 밖으로 나갈경우, 나간 블럭 전부 삭제 */
                    if (isDisappeared == true && !selectedBlock) {
                        thisBlock.deleteLowerDepthChildBlocks();

                    /** 블록이 화면 밖으로 나가지 않고 연결되는 경우 */
                    } else {
                        var isConntected = true;
                        /** 어떤 블록의 DOWN이나 INDENT로 조립되지 않는 경우 */
                        if (!selectedBlock) {
                            /** 이동한 block이 rootblock일 경우 */
                            if ( thisBlock.getPrevBlock() == null ) {
                     
                                isConntected = false;
                                selectedBlock = blockContainerThis.getRootToLastBottomBlock();

                                
                                if (blockContainerThis.getNodeBlockList().length == 1) {
                                    var rootBlockContainerDom = blockContainerThis.getBlockContainerDom();
                                    $(rootBlockContainerDom).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SHADOWBLOCK_CONTAINER).remove();
                                    $blockNewMainDom.remove();
                                  
                                    thisBlock.setMovedBlockListOpacity(1);
                                    var blockList = blockContainerThis.getBlockList();
                                    blockList.forEach(block => {
                                        block.renderBlockHolderShadow(STR_NONE);
                                        block.renderSelectedBlockColor(false);
                                        $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SUB_BTN_CONTAINER).remove();
                                    });
                                    // $blockNewMainDom.remove();
                                    // console.log('여기');
                                    return;
                                } else {
                                    thisBlock.removeRootBlock();
                                    thisBlock.setDirection(BLOCK_DIRECTION.DOWN);
                                }
                            
                            }
                            /** 이동한 block의 prevBlock이 rootblock일 경우 */
                            else if ( thisBlock.getPrevBlock().getUUID() == blockContainerThis.getRootBlock().getUUID() ) {
                                isConntected = false;
                                selectedBlock = blockContainerThis.getRootToLastBottomBlock();

                            /** 이동한 block의 prevBlock이 rootblock이 아닐 경우 */
                            } else {
                
                                isConntected = false;
                                var lastBottomBlock = blockContainerThis.getRootToLastBottomBlock();
                           
                                /** 이동한 Block 하위에, Board에 놓여 있는 맨 마지막 Block이 포함되어 있는 경우 */
                                var isFinalBlock = thisBlock.getChildLowerDepthBlockList().some(block => {
                                    if ( block.getUUID() == lastBottomBlock.getUUID() ) {
                                        selectedBlock = thisBlock.getPrevBlock();
                                        return true;
                                    }
                                });
                          
                                /** 이동하는 하위 depth Block 들이 
                                 *  board에 놓여있는 block들의 맨 마지막 위치에 있는 block이 아닐 경우
                                 */
                                if (isFinalBlock == false) {
                                    selectedBlock = lastBottomBlock;
                                }
                            }
                        }

                        /** 어떤 블록의 DOWN이나 INDENT로 조립되지 않는 경우 */
                        if (isConntected == false) {
                            selectedBlock.appendBlock(thisBlock, BLOCK_DIRECTION.DOWN);
                           
                        /** 특정 블록의 DOWN이나 INDENT로 조립된 경우 */ 
                        } else {
                            /** 이동한 block이 rootblock일 경우 */
                            if ( thisBlock.getPrevBlock() == null ) {
                                thisBlock.removeRootBlock();
                            }
                            selectedBlock.appendBlock(thisBlock, selectedBlockDirection);
                        }
                    }

                    thisBlock.renderRemoveDom($blockOldMainDom, $moveChildListDom);
                    /** 이동하는 하위 depth Block 들의 opacity 1로 변경 */
                    thisBlock.setMovedBlockListOpacity(1);

                    var rootBlockContainerDom = blockContainerThis.getBlockContainerDom();
                    $(rootBlockContainerDom).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SHADOWBLOCK_CONTAINER).remove();

                    if (isOnlyRootBlockAtBoard == true) {
                        thisBlock.setDirection(BLOCK_DIRECTION.ROOT);
                    } 
             
                    blockContainerThis.stopDragBlock(true, thisBlock); 
            
                    $blockNewMainDom.remove();
                    nowMovedBlockList = [];
                    shadowBlock = null;
                }
            });
        // }
    }

    Block.prototype.removeRootBlock = function() {
        this.getChildLowerDepthBlockList();
        var lastChildBlock = this.getLastChildBlock();
        var nextBlockList = lastChildBlock.getNextBlockList();
        lastChildBlock.setNextBlockList([]);
        nextBlockList.some(nextBlock => {
            nextBlock.setPrevBlock(null);
            nextBlock.setDirection(BLOCK_DIRECTION.ROOT);
        });
    }

    Block.prototype.createSubButton = function() {
        var thisBlock = this;
        var blockContainerThis = thisBlock.getBlockContainerThis();
        var blockMainDom = thisBlock.getBlockMainDom();
        var blockCodeLineType = thisBlock.getBlockCodeLineType();
   
        var _bindElse = function(isFinally) {
            var STATE;
            if (isFinally == true) {
                STATE = STATE_isFinally;
            } else {
                STATE = STATE_isIfElse;
            }
            /** else가 존재하는 경우 -> else 삭제*/
            if (thisBlock.getState(STATE) == true) {
                var elseBlock = thisBlock.ifElseBlock;
                elseBlock.deleteLowerDepthChildBlocks();
                thisBlock.ifElseBlock = null;
                blockContainerThis.reRenderBlockList();
                blockContainerThis.renderBlockLineNumberInfoDom(true);

                thisBlock.setState({
                    [STATE]: false
                });
            /** else가 존재하지 않는 경우 -> else 생성*/
            } else {
                var selectedBlock;
                var newBlock;
                if (isFinally == true) {
                    if (thisBlock.ifElseBlock) {
                        selectedBlock = thisBlock.ifElseBlock;
                    } else {
                        selectedBlock = thisBlock.getLastElifBlock();
                    }
                    newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.FINALLY );
                } else {
                    selectedBlock = thisBlock.getLastElifBlock();
                    newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.ELSE );
                }

                newBlock.renderSelectedBlockColor(true);
    
                selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                thisBlock.ifElseBlock = newBlock;

                blockContainerThis.reRenderAllBlock_asc();
                thisBlock.setState({
                    [STATE]: true
                });
            }
        }

        var elseOnOffStr = STR_NULL;
        if (thisBlock.getState(STATE_isIfElse) == true) {
            elseOnOffStr = 'off';
        } else {
            elseOnOffStr = 'on';
        }

        if (blockCodeLineType == BLOCK_CODELINE_TYPE.IF) {
            var containerButton = $(`<div class='${VP_CLASS_STYLE_FLEX_ROW_BETWEEN}
                                                 ${VP_CLASS_BLOCK_SUB_BTN_CONTAINER}'>
                                        </div>`);
                                    
            var plusElifButton = $(`<div class='vp-apiblock-plus-elif-button'>+ elif</div>'`);
            var toggleElseButton = $(`<div class='vp-apiblock-toggle-else-button'> else ${elseOnOffStr} </div>`);
            containerButton.append(plusElifButton);
            containerButton.append(toggleElseButton);
            $(blockMainDom).append(containerButton);
            $(plusElifButton).click(function(plusElifEvent) {
                var selectedBlock = thisBlock.getLastElifBlock();
                // var selectedBlock = thisBlock.getLastElifBlock() || thisBlock;
                // console.log('selectedBlock',selectedBlock.getUUID());
                var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.ELIF);
                thisBlock.setLastElifBlock(newBlock);
                selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);

                var elifConditionCode = GenerateIfConditionList(newBlock, BLOCK_CODELINE_TYPE.ELIF);
                newBlock.writeCode(elifConditionCode);
                blockContainerThis.reRenderAllBlock_asc();
                newBlock.renderSelectedBlockColor(true);
                plusElifEvent.stopPropagation();
            });
            $(toggleElseButton).click(function() {
                _bindElse();
            });
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.FOR) {
            var containerButton = $(`<div class='${VP_CLASS_STYLE_FLEX_ROW_END}
                                                 ${VP_CLASS_BLOCK_SUB_BTN_CONTAINER}'>
                                      </div>`);
   
            var toggleElseButton = $(`<div class='vp-apiblock-toggle-else-button'> else ${elseOnOffStr} </div>`);
            containerButton.append(toggleElseButton);
            $(blockMainDom).append(containerButton);
            $(toggleElseButton).click(function() {
                _bindElse();
            });
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.TRY) {
            var finallyOnOffStr = STR_NULL;
            if (thisBlock.getState(STATE_isFinally) == true) {
                finallyOnOffStr = 'off';
            } else {
                finallyOnOffStr = 'on';
            }
            var containerButton = $(`<div class='${VP_CLASS_STYLE_FLEX_ROW_BETWEEN}
                                                 ${VP_CLASS_BLOCK_SUB_BTN_CONTAINER}' >
                                        </div>`);

            var plusElifButton = $(`<div class='vp-apiblock-plus-elif-button'> + except </div>'`);
            var toggleElseButton = $(`<div class='vp-apiblock-toggle-else-button'> else ${elseOnOffStr} </div>`);
            var finallyButton = $(`<div class='vp-apiblock-toggle-else-button'> finally ${finallyOnOffStr} </div>`);

            containerButton.append(plusElifButton);
            containerButton.append(toggleElseButton);
            containerButton.append(finallyButton);

            $(blockMainDom).append(containerButton);

            $(plusElifButton).click(function(plusElifEvent) {
                var selectedBlock = thisBlock.getLastElifBlock();
                // var selectedBlock = thisBlock.getLastElifBlock() || thisBlock;
                var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.EXCEPT);
                thisBlock.setLastElifBlock(newBlock);

                selectedBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);

                var elifConditionCode = GenerateIfConditionList(newBlock, BLOCK_CODELINE_TYPE.EXCEPT);
                newBlock.writeCode(elifConditionCode);

                blockContainerThis.reRenderAllBlock_asc();
                newBlock.renderSelectedBlockColor(true);
                plusElifEvent.stopPropagation();
            });

            $(toggleElseButton).click(function() {
                _bindElse();
            });

            $(finallyButton).click(function() {
                _bindElse(true);
            });
        } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.BLANK
                    || blockCodeLineType == BLOCK_CODELINE_TYPE.NODE
                    || blockCodeLineType == BLOCK_CODELINE_TYPE.TEXT) {
            return;
        }   
    }

    /**
     * @async
     * block click시 발생하는 이벤트 메소드 
     */
    Block.prototype.bindClickEvent = function() {

        var thisBlock = this;
        var blockContainerThis = thisBlock.getBlockContainerThis();
        var blockMainDom = thisBlock.getBlockMainDom();
        var blockCodeLineType = thisBlock.getBlockCodeLineType();

        $(blockMainDom).off(STR_CLICK);
        $(blockMainDom).single_double_click( function(event){
            // '클릭';
            if ( blockContainerThis.getFocusedPageType() == FOCUSED_PAGE_TYPE.EDITOR
                 && blockCodeLineType == BLOCK_CODELINE_TYPE.NODE
                 && thisBlock.getIsNodeBlockInput() == false) {
                var childLowerDepthBlockList = thisBlock.getChildLowerDepthBlockList();
                var selectBlock = blockContainerThis.getSelectedBlock();
                // var is = false;
                if (selectBlock) {
                    if (selectBlock.getUUID() == thisBlock.getUUID()) {
    
                    } else {
                        var findedNodeBlock = blockContainerThis.findNodeBlock(selectBlock);
                        if (findedNodeBlock.getUUID() == thisBlock.getUUID()) {
                            if (thisBlock.getIsNodeBlockInput() != true) {
                                blockContainerThis.resetBlockList();
                            } 
                
                            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SUB_BTN_CONTAINER)).remove();
                
                            thisBlock.createSubButton();
                            thisBlock.renderMyColor(true);
                            thisBlock.setIsClicked(true);
                
                            blockContainerThis.setSelectedBlock(thisBlock);
                            blockContainerThis.renderBlockOptionTab();
                            blockContainerThis.openOptionPopup();
    
                            event.stopPropagation();
                            return;
                        }
                    }
           
                    // is = childLowerDepthBlockList.some( (childBlock, index) => {
                    //     if (selectBlock.getUUID() == childBlock.getUUID()) {
                    //         return true;
                    //     }
                    // });
                }

                // if (is == true) {
                //     return;
                // }

                childLowerDepthBlockList.forEach( (block,index) => {
                    if (index != 0) {
                        if (thisBlock.getIsNodeBlockToggled() == true) {
                            if (block.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.HOLDER) {
                                $(block.getBlockMainDom()).addClass('vp-apiblock-style-display-flex');
                                $(block.getBlockMainDom()).removeClass('vp-apiblock-style-display-none');
                            }
                        } else {
                            $(block.getBlockMainDom()).addClass('vp-apiblock-style-display-none');
                            $(block.getBlockMainDom()).removeClass('vp-apiblock-style-display-flex');
                        }
                    }
                });

                if (thisBlock.getIsNodeBlockToggled() == true) {
                    thisBlock.setIsNodeBlockToggled(false);
                    $(thisBlock.getBlockMainDom()).css(STR_BOX_SHADOW, STR_NONE);
                } else {
                    thisBlock.setIsNodeBlockToggled(true);
                    $(thisBlock.getBlockMainDom()).css(STR_BOX_SHADOW, '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)');
                }

            } else {

                var childLowerDepthBlockList = thisBlock.getChildLowerDepthBlockList();
                childLowerDepthBlockList.forEach( (block,index) => {
                    if (block.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.HOLDER) {
                        $(block.getBlockMainDom()).addClass('vp-apiblock-style-display-flex');
                        $(block.getBlockMainDom()).removeClass('vp-apiblock-style-display-none');
                    }
                });
                thisBlock.setIsNodeBlockToggled(false);
                blockContainerThis.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
            }

            if (thisBlock.getIsNodeBlockInput() != true) {
                blockContainerThis.resetBlockList();
            } 

            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SUB_BTN_CONTAINER)).remove();

            thisBlock.createSubButton();
            thisBlock.renderMyColor(true);
            thisBlock.setIsClicked(true);

            blockContainerThis.setSelectedBlock(thisBlock);
            blockContainerThis.renderBlockOptionTab();
            blockContainerThis.openOptionPopup();

            event.stopPropagation();
        }, function () {
            // console.log('더블클릭');
            if (blockCodeLineType == BLOCK_CODELINE_TYPE.NODE) {
                var blockUUID = thisBlock.getUUID();
                thisBlock.setIsNodeBlockInput(true);
                $(`.vp-apiblock-nodeblock-input-${blockUUID}`).css(STR_DISPLAY, STR_BLOCK);
                $(`.vp-apiblock-nodeblock-input-${blockUUID}`).val(thisBlock.getState(STATE_codeLine))
                $(`.vp-apiblock-nodeblock-${blockUUID}`).css(STR_DISPLAY, STR_NONE);
    
                $(document).off(STR_CHANGE_KEYUP_PASTE,  vpCommon.wrapSelector(vpCommon.formatString(".{0}",`vp-apiblock-nodeblock-input-${blockUUID}`)));
                $(document).on(STR_CHANGE_KEYUP_PASTE, vpCommon.wrapSelector(vpCommon.formatString(".{0}",`vp-apiblock-nodeblock-input-${blockUUID}`)), function(event) {
                    var inputValue = $(this).val();
                    thisBlock.setState({
                        [STATE_codeLine]: inputValue
                    });
                    $(`.vp-apiblock-nodeblock-input-${blockUUID}`).val(inputValue);
                    $(`.vp-apiblock-nodeblock-${blockUUID}`).text(inputValue);
                    thisBlock.renderOptionPage();
                });
             
            } else if (blockCodeLineType == BLOCK_CODELINE_TYPE.TEXT) {
                /** TEXT 블럭은 더블클릭해도 아무런 작용을 하지 않음 */
            } else {
                thisBlock.runThisBlock();
            }
        });
    }

    /** block을 x 버튼을 눌러 삭제할 때 실행되는 메소드 */
    Block.prototype.clickBlockDeleteButton = function() {
        var blockContainerThis = this.getBlockContainerThis();

        this.deleteLowerDepthChildBlocks();
        this.resetOptionPage();

        blockContainerThis.reRenderAllBlock_asc();
        blockContainerThis.closeOptionPopup(this);
    }

    /** block shadow를 삭제하거나 만드는 메소드  */
    Block.prototype.renderBlockHolderShadow = function(NONE_OR_BLOCK) {
        if ( this.getHolderBlock() ) {
            $( this.getHolderBlock().getBlockMainDom() ).css(STR_DISPLAY, NONE_OR_BLOCK);
        }
        var blockLeftHolderDom = this.getBlockLeftHolderDom();
        $(blockLeftHolderDom).css(STR_DISPLAY, NONE_OR_BLOCK);
    }


    /** Block Editor에 Scroll이 생성 될지 안 될지 결정하는 메소드
     *   0% ~70% 고정
     *   70% ~ 100% 상위로 이동 화면 scroll 조정 함
    */
    Block.prototype.renderEditorScrollTop = function(isNewBlock) {
        // var blockContainerThis = this.getBlockContainerThis();
        // var blockChildList = blockContainerThis.getRootBlock().getChildBlockList();
        
        // var minusIndex = 0;
        // var blockNumber = 0;

        // blockChildList.some((block, index) => {
        //     if (block.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.HOLDER) {
        //         if (this.getUUID() == block.getUUID()) {
        //             blockNumber = index - minusIndex;
        //             return true;
        //         }
        //     } else {
        //         minusIndex++;
        //     }
        // });

        // var maxHeight = blockContainerThis.getMaxHeight();
        // var scrollHeight = blockContainerThis.getScrollHeight();

        // if (scrollHeight >= maxHeight) {
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_SCROLLBAR)).css(STR_OVERFLOW_X, STR_HIDDEN);
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_SCROLLBAR)).css(STR_OVERFLOW_Y, STR_AUTO);

        // } else {
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_SCROLLBAR)).css(STR_OVERFLOW_X, STR_HIDDEN);
        //     $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_SCROLLBAR)).css(STR_OVERFLOW_Y, STR_HIDDEN);
        // }
        
        // var eventClientY = blockContainerThis.getEventClientY();
        // if (isNewBlock == true) {
         
        // } else if (eventClientY < $(window).height() * 0.7) {
        //     return;
        // }

        // var thisBlockFromRootBlockHeight = 0;
        // while(blockNumber != 0) {
        //     blockNumber--;
        //     thisBlockFromRootBlockHeight += NUM_BLOCK_MARGIN_TOP_PX;
        //     thisBlockFromRootBlockHeight += NUM_BLOCK_HEIGHT_PX;
        //     thisBlockFromRootBlockHeight += NUM_BLOCK_MARGIN_BOTTOM_PX;
        // }

        // if (thisBlockFromRootBlockHeight == 0) {
        //     thisBlockFromRootBlockHeight = blockContainerThis.getThisBlockFromRootBlockHeight();
        //      $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).animate({
        //         scrollTop: thisBlockFromRootBlockHeight 
        //     }, 100);
        //     return;
        // } else {
        //     blockContainerThis.setThisBlockFromRootBlockHeight(thisBlockFromRootBlockHeight);  
        // }
    
        // $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).scrollTop(thisBlockFromRootBlockHeight);
    }

    /** this Block 부터 코드 실행 */
    Block.prototype.runThisBlock = function() {
        var thisBlock = this;
        var blockContainerThis = thisBlock.getBlockContainerThis();
        blockContainerThis.setIsBlockDoubleClicked(true);
        var code = blockContainerThis.makeCode(thisBlock);
        if (thisBlock.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.TEXT) {
            /** validation 걸릴 때 */
            if (code.indexOf('BREAK_RUN') != -1) {
                return;
            }
            blockContainerThis.setAPIBlockCode(code);
            blockContainerThis.generateCode(true);
        }

    }

    /**
     * Block Left Holder dom의 height 계산
     */
    Block.prototype.renderBlockLeftHolderHeight = function() {
        var block = this;
        var leftHolderClientRect = $(block.getBlockLeftHolderDom())[0].getBoundingClientRect();
        var holderBlock = block.getHolderBlock();
        var holderBlockClientRect = $(holderBlock.getBlockMainDom())[0].getBoundingClientRect();
 
        var distance = holderBlockClientRect.y - leftHolderClientRect.y;

        $(block.getBlockLeftHolderDom()).css(STR_HEIGHT, distance);
        block.setTempBlockLeftHolderHeight(distance);
    }
 
    /** api 블럭만 사용하는 메소드 */
    Block.prototype.setFuncID = function(funcID) {
        this.funcID = funcID;
    }
    Block.prototype.getFuncID = function() {
        return this.funcID;
    }

    Block.prototype.setOptionPageLoadCallback = function(optionPageLoadCallback) {
        this.optionPageLoadCallback = optionPageLoadCallback;
    }
    Block.prototype.getOptionPageLoadCallback = function() {
        return this.optionPageLoadCallback;
    }

    Block.prototype.setLoadOption = function(loadOption) {
        this.loadOption = loadOption;
    }
    Block.prototype.getLoadOption = function() {
        return this.loadOption;
    }

    Block.prototype.setImportPakage = function(importPakage) {
        this.importPakage = importPakage;
    }
    Block.prototype.getImportPakage = function() {
        return this.importPakage;
    }

    Block.prototype.setBlockOptionPageDom = function(blockOptionPageDom) {
        this.blockOptionPageDom = blockOptionPageDom;
    }

    Block.prototype.getBlockOptionPageDom = function() {
        return this.blockOptionPageDom;
    }

    return {
        Block
    };
});
