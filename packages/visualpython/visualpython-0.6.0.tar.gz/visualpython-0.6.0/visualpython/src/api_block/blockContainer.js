define([
    'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/common/metaDataHandler'
    , 'nbextensions/visualpython/src/common/constant'

    , './shadowBlock.js'
    , './api.js'
    , './api_list.js'
    , './constData.js'
    , './block.js'
    , './blockRenderer.js'
], function ( vpCommon, vpFuncJS, md, vpConst,
              shadowBlock, api, api_list, constData, block, blockRenderer ) {

    const { ChangeOldToNewState
            , UpdateOneArrayValueAndGet
            , DeleteOneArrayValueAndGet

            , DestructureFromBlockArray
            , RemoveSomeBlockAndGetBlockList

            , MakeFirstCharToUpperCase
            , FindStateValue
            , MapTypeToName
            , ControlToggleInput
        
            , IsCodeBlockType
            , IsCanHaveIndentBlock } = api;

    const {  BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK
            , FOCUSED_PAGE_TYPE

            , STR_CHANGE_KEYUP_PASTE
            , STR_COLON_SELECTED 

            , VP_CLASS_PREFIX 

            , VP_CLASS_BLOCK_NUM_INFO
            , VP_CLASS_BLOCK_CONTAINER

            , VP_CLASS_BLOCK_HEADER_PARAM
            , VP_CLASS_APIBLOCK_MAIN
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_CODELINE_ELLIPSIS
            , VP_CLASS_APIBLOCK_INPUT_PARAM
            , VP_CLASS_APIBLOCK_PARAM_PLUS_BTN
            , VP_CLASS_APIBLOCK_PARAM_DELETE_BTN
            , VP_CLASS_APIBLOCK_MENU_BTN
            , VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW
            , VP_CLASS_BLOCK_SUB_BTN_CONTAINER
            , VP_CLASS_SELECTED_SHADOWBLOCK 

            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_DEFAULT_POS_Y
            , NUM_DEFAULT_POS_X
            , NUM_MAX_BLOCK_NUMBER
            , NUM_BLOCK_MAX_WIDTH
            , NUM_TEXT_BLOCK_WIDTH
            , NUM_OPTION_PAGE_WIDTH

            , STR_NULL
            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_ONE_SPACE
            , STR_DOT
            , STR_SCROLLHEIGHT
            , STR_DATA_NUM_ID
            , STR_PX
            , STR_BORDER
            , STR_HEIGHT
            , STR_SPAN
            , STR_WIDTH
            , STR_MARGIN_LEFT
            , STR_MAX_WIDTH
            , STR_KEYWORD_NEW_LINE
            , STR_ONE_INDENT
            , STR_CLICK
            , STR_COLOR
            , STR_BACKGROUND_COLOR 
            , STR_DATA_DEPTH_ID 

            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_CODE
            , STR_PROPERTY
            , STR_OPACITY
            , STR_MSG_AUTO_GENERATED_BY_VISUALPYTHON
  
            , STR_DISPLAY
            , STR_BLOCK
            , STR_RIGHT
            , STR_NONE 
            , STR_FLEX 

            , STATE_classInParamList
            , STATE_defInParamList
            , STATE_returnOutParamList

            , STATE_elifCodeLine
            , STATE_exceptCodeLine

            , STATE_breakCodeLine
            , STATE_continueCodeLine
            , STATE_passCodeLine
            , STATE_codeLine
            , STATE_propertyCodeLine
   

            , STATE_isIfElse
            , STATE_isForElse
            , STATE_isFinally

            , STATE_optionState

            , COLOR_CLASS_DEF
            , COLOR_CONTROL
            , COLOR_CODE
            , COLOR_FOCUSED_PAGE
            , COLOR_WHITE
            , API_BLOCK_PROCESS_DEVELOPMENT
        
            , ERROR_AB0002_INFINITE_LOOP } = constData;
 
    const { Block } = block;
    const { RenderFocusedPage
            , RenderBlockMainDom
            , RenderBlockLeftHolderDom
            , RenderBlockMainInnerDom
            , RenderBlockMainHeaderDom

            , RenderDeleteBlockButton


            , RenderHTMLDomColor } = blockRenderer;
         
    const ShadowBlock = shadowBlock; 
    const { api_listInit } = api_list;

    var BlockContainer = function() {
        this.importPackageThis = null;
        this.blockList = [];
        this.nodeBlockList = [];
        this.textBlockList = [];
        this.prevBlockList = [];
        this.nowMovedBlockList = [];
        this.blockHistoryStack = [];
        this.blockHistoryStackCursor = 0;

        this.resetBlockListButton = null;

        this.isDebugMode = false; 
        this.isBlockDoubleClicked = false;
        this.isMenubarOpen = false;
        this.isShowDepth = true;
        this.isOptionPageOpen = true;
        this.isAPIListPageOpen = false;
        this.isOptionPageResize = false;

        this.focusedPageType = FOCUSED_PAGE_TYPE;
        this.classNum = 1;
        this.defNum = 1;
        this.forNum = 1;
        this.nodeBlockNumber = 0;

        this.thisBlockFromRootBlockHeight = 0;
        this.eventClientY = 0;
        this.optionPageWidth = NUM_OPTION_PAGE_WIDTH;
        this.selectedBlock = null;

        this.blockContainerDom = null;
        this.code = STR_NULL;

        this.mdHandler = null;  
        this.loadedVariableList = [];

        this.domPool = new Map();
    }

    BlockContainer.prototype.setMetahandler = function(funcID) {
        this.mdHandler = new md.MdHandler(funcID); 
    }

    BlockContainer.prototype.setImportPackageThis = function(importPackageThis) {
        this.importPackageThis = importPackageThis;
    }

    BlockContainer.prototype.getImportPackageThis = function() {
        return this.importPackageThis;
    }

    BlockContainer.prototype.setIsBlockDoubleClicked = function(isBlockDoubleClicked) {
        this.isBlockDoubleClicked = isBlockDoubleClicked;
    }

    BlockContainer.prototype.getIsBlockDoubleClicked = function() {
        return this.isBlockDoubleClicked;
    }

    BlockContainer.prototype.setIsMenubarOpen = function(isMenubarOpen) {
        this.isMenubarOpen = isMenubarOpen;
    }
    BlockContainer.prototype.getIsMenubarOpen = function() {
        return this.isMenubarOpen;
    }

    BlockContainer.prototype.setIsShowDepth = function(isShowDepth) {
        this.isShowDepth = isShowDepth;
    }
    BlockContainer.prototype.getIsShowDepth = function() {
        return this.isShowDepth;
    }

    BlockContainer.prototype.setIsOptionPageOpen = function(isOptionPageOpen) {
        this.isOptionPageOpen = isOptionPageOpen;
    }
    BlockContainer.prototype.getIsOptionPageOpen = function() {
        return this.isOptionPageOpen;
    }

    BlockContainer.prototype.setIsAPIListPageOpen = function(isAPIListPageOpen) {
        this.isAPIListPageOpen = isAPIListPageOpen;
    }
    BlockContainer.prototype.getIsAPIListPageOpen = function() {
        return this.isAPIListPageOpen;
    }
    
    BlockContainer.prototype.setOptionPageWidth = function(optionPageWidth) {
        this.optionPageWidth = optionPageWidth;
    }
    BlockContainer.prototype.getOptionPageWidth = function() {
        return this.optionPageWidth;
    }

    BlockContainer.prototype.setOptionPageResize = function(isOptionPageResize) {
        this.isOptionPageResize = isOptionPageResize;
    }
    BlockContainer.prototype.getOptionPageResize = function() {
        return this.isOptionPageResize;
    }

    /** Block 생성 */
    BlockContainer.prototype.createBlock = function(blockCodeLineType, isMetadata, blockData) {
        return new Block(this, blockCodeLineType, isMetadata, blockData);
    }

    /** block을 blockList에 add */
    BlockContainer.prototype.addBlock = function(block) {
        this.blockList = [...this.blockList, block];
    }

    /** blockList를 가져옴*/
    BlockContainer.prototype.getBlockList = function() {
        return this.blockList;
    }
    /** blockList를 파라미터로 받은 blockList로 덮어 씌움*/
    BlockContainer.prototype.setBlockList = function(blockList) {
        this.blockList = blockList;
    }

    BlockContainer.prototype.getNodeBlockList = function() {
        return this.nodeBlockList;
    }

    BlockContainer.prototype.getNodeBlockList_asc = function() {
        var rootBlock = this.getRootBlock();
        var blockChildList = rootBlock.getChildBlockList();
        var nodeBlockList = [];
        blockChildList.forEach((block, index) => {
            if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE) {
                nodeBlockList.push(block);
            } 
        });
        return nodeBlockList;
    }

    BlockContainer.prototype.getNodeBlockAndTextBlockList_asc = function() {
        var rootBlock = this.getRootBlock();
        var blockChildList = rootBlock.getChildBlockList();
        var nodeBlockList = [];
        blockChildList.forEach((block, index) => {
            if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE
                || block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
                nodeBlockList.push(block);
            } 
        });
        return nodeBlockList;
    }

    BlockContainer.prototype.setNodeBlockList = function(nodeBlockList) {
        this.nodeBlockList = nodeBlockList;
    }

    /** block을 blockList에 add */
    BlockContainer.prototype.addNodeBlock = function(block) {
        this.addNodeBlockNumber();
        this.nodeBlockList = [...this.nodeBlockList, block];
    }

    BlockContainer.prototype.getTextBlockList = function() {
        return this.textBlockList;
    }
    BlockContainer.prototype.setTextBlockList = function(textBlockList) {
        this.textBlockList = textBlockList;
    }
    /** block을 blockList에 add */
    BlockContainer.prototype.addTextBlock = function(block) {
        this.textBlockList = [...this.textBlockList, block];
    }
    
    /** prevBlockList를 가져옴*/
    BlockContainer.prototype.getPrevBlockList = function() {
        return this.prevBlockList;
    }
    /** prevBlockList를 파라미터로 받은 prevBlockList로 덮어 씌움*/
    BlockContainer.prototype.setPrevBlockList = function(prevBlockList) {
        this.prevBlockList = prevBlockList;
    }
    
    /** NowMovedBlockList를 가져옴*/
    BlockContainer.prototype.getNowMovedBlockList = function() {
        return this.nowMovedBlockList;
    }
    /** NowMovedBlockList를 파라미터로 받은 NowMovedBlockList로 덮어 씌움*/
    BlockContainer.prototype.setNowMovedBlockList = function(nowMovedBlockList) {
        this.nowMovedBlockList = nowMovedBlockList;
    }

    /** blockHistoryStack를 가져옴 */
    BlockContainer.prototype.getBlockHistoryStack = function() {
        return this.blockHistoryStack;
    }
    BlockContainer.prototype.getBlockLastHistoryStack = function() {
        return this.blockHistoryStack[this.blockHistoryStackCursor-1];
    }
    /** blockHistoryStack를 파라미터로 받은 blockHistoryStack로 덮어 씌움 */
    BlockContainer.prototype.setBlockHistoryStack = function(blockHistoryStack) {
        this.blockHistoryStack = blockHistoryStack;
    }

    /** blockHistoryStack에 최신 데이터를 push */
    BlockContainer.prototype.pushBlockHistoryStack = function(blockStack) {
        this.blockHistoryStack.push(blockStack);
        this.blockHistoryStackCursor += 1;
    }

    /** blockHistoryStack에 최신 데이터를 pop */
    BlockContainer.prototype.popBlockHistoryStackAndGet = function() {
        if (this.blockHistoryStackCursor < 0) {
            return;
        }
        this.blockHistoryStackCursor -= 1;
    }
    
    /** blockHistoryStack을 리셋합니다  */
    BlockContainer.prototype.resetStack = function() {
        this.blockHistoryStack = [];
    }

    /** root block을 get */
    BlockContainer.prototype.getRootBlock = function() {
        var blockList = this.getBlockList();
        var rootBlock = null;
        blockList.some(block => {
            if (block.getDirection() == BLOCK_DIRECTION.ROOT) {
                rootBlock = block;
                return true;
            }
        });
        return rootBlock;
    }

    BlockContainer.prototype.setClassNum = function(classNum) {
        this.classNum = classNum;
    }
    BlockContainer.prototype.addClassNum = function() {
        this.classNum += 1;
    }
    BlockContainer.prototype.getClassNum = function() {
        return this.classNum;
    }

    BlockContainer.prototype.setDefNum = function(defNum) {
        this.defNum = defNum;
    }
    BlockContainer.prototype.addDefNum = function() {
        this.defNum += 1;
    }
    BlockContainer.prototype.getDefNum = function() {
        return this.defNum;
    }

    BlockContainer.prototype.setForNum = function(forNum) {
        this.forNum = forNum;
    }
    BlockContainer.prototype.addForNum = function() {
        this.forNum += 1;
    }
    BlockContainer.prototype.getForNum = function() {
        return this.forNum;
    }

    BlockContainer.prototype.setNodeBlockNumber = function(nodeBlockNumber) {
        this.nodeBlockNumber = nodeBlockNumber;
    }
    BlockContainer.prototype.addNodeBlockNumber = function() {
        this.nodeBlockNumber += 1;
    }
    BlockContainer.prototype.getNodeBlockNumber = function() {
        return this.nodeBlockNumber;
    }

    BlockContainer.prototype.getMaxWidth = function() {
        var maxWidth = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).width();
        return maxWidth;
    }

    BlockContainer.prototype.getMaxHeight = function() {
        var maxHeight = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).height();
        return maxHeight;
    }

    BlockContainer.prototype.getScrollHeight = function() {
        var scrollHeight = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).prop(STR_SCROLLHEIGHT);
        return scrollHeight;
    }

    BlockContainer.prototype.setThisBlockFromRootBlockHeight = function(thisBlockFromRootBlockHeight) {
        this.thisBlockFromRootBlockHeight = thisBlockFromRootBlockHeight;
    }
    BlockContainer.prototype.getThisBlockFromRootBlockHeight = function() {
        return this.thisBlockFromRootBlockHeight;
    }

    BlockContainer.prototype.setCurrCursorY = function(eventClientY) {
        this.eventClientY = eventClientY;
    }
    BlockContainer.prototype.getEventClientY = function() {
        return this.eventClientY;
    }

    BlockContainer.prototype.setResetBlockListButton = function(resetBlockListButton) {
        this.resetBlockListButton = resetBlockListButton;
    }
    BlockContainer.prototype.getResetBlockListButton = function() {
        return this.resetBlockListButton;
    }

    BlockContainer.prototype.setBlockContainerDom = function(blockContainerDom) {
        this.blockContainerDom = blockContainerDom;
    }
    BlockContainer.prototype.getBlockContainerDom = function() {
        return this.blockContainerDom;
    }

    BlockContainer.prototype.setSelectedBlock = function(selectedBlock) {
        this.selectedBlock = selectedBlock;
    }
    BlockContainer.prototype.getSelectedBlock = function() {
        return this.selectedBlock;
    }

    BlockContainer.prototype.getAPIBlockCode = function() {
        return this.code;
    }
    BlockContainer.prototype.setAPIBlockCode = function(code) {
        this.code = code;
    }
    
    BlockContainer.prototype.setFocusedPageType = function(focusedPageType) {
        this.focusedPageType = focusedPageType;
    }
    BlockContainer.prototype.getFocusedPageType = function() {
        return this.focusedPageType;
    }

    BlockContainer.prototype.setFocusedPageTypeAndRender = function(focusedPageType) {
        this.setFocusedPageType(focusedPageType);
        RenderFocusedPage(focusedPageType);
    }

    BlockContainer.prototype.setCtrlSaveData = function() {
        var selectedBlock = this.getSelectedBlock();
        var lastBlock = selectedBlock.getLastChildBlock();
        var childBlockList = selectedBlock.getChildLowerDepthBlockList();

        var blockList_cloned = this.copyBlockList(childBlockList, lastBlock);
        var lastCopyBlocklist_cloned = blockList_cloned[0];

        this.lastBlock = lastBlock;
        this.lastCopyBlocklist_cloned = lastCopyBlocklist_cloned;
    }

    BlockContainer.prototype.getCtrlSaveData = function() {
        return {
            lastBlock: this.lastBlock
            , lastCopyBlocklist_cloned: this.lastCopyBlocklist_cloned
        }
    }
    /** blockList에서 특정 block을 삭제
     * @param {string} blockUUID
     */
    BlockContainer.prototype.deleteBlock = function(blockUUID) {
        /** blockList를 돌며 삭제하고자 하는 block을 찾음.
         *  block은 고유의 UUID 
         *  파라미터로 들어온 block의 UUID가 blockList의 UUID와 일치하는 블럭이 있는지 찾는 과정.
         *  찾으면 isBlock true, blockList에서 index를 얻음
         *  못찾으면 isBlock false, 아무것도 하지 않고 메소드 작업을 종료.
         */
        var blockList = this.getBlockList();
        blockList.some((block, index) => {
            if (block.getUUID() == blockUUID) {
                delectedIndex = index;
                blockList.splice(index, 1);
                return true;
            } else {
                return false;
            }
        });
    }
    /** nodeBlockList에서 특정 block을 삭제
     * @param {string} blockUUID
     */
    BlockContainer.prototype.deleteNodeBlock = function(blockUUID) {
        var nodeBlockList = this.getNodeBlockList();
        nodeBlockList.some((block, index) => {
            if (block.getUUID() == blockUUID) {
                delectedIndex = index;
                nodeBlockList.splice(index, 1);
                return true;
            } else {
                return false;
            }
        });
    }

    /** run 버튼 실행시 코드 실행 */
    BlockContainer.prototype.makeAllCode = function() {
        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return;
        }

        var codeLineStr = STR_NULL;
        var rootToChildBlockList = rootBlock.getRootToChildBlockList();

        var rootDepth = rootBlock.getDepth();
        rootToChildBlockList.forEach( block => {
            if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
                return;
            }
            /** 각 Block의 blockCodeLine에 맞는 코드 생성 */
            var currBlock = block;
            var indentString = currBlock.getIndentString(rootDepth);
            var codeLine = currBlock.setCodeLineAndGet(indentString);

            /**  코드 라인 한 칸 띄우기 */    
            codeLine += STR_KEYWORD_NEW_LINE;
            codeLineStr += codeLine;
        });

        this.setAPIBlockCode(codeLineStr);
        return codeLineStr;
    }

    BlockContainer.prototype.makeAPIBlockMetadata = function() {
        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return [];
        }

        var nextBlockList = rootBlock.getNextBlockList();
        var stack = [];

        if (nextBlockList.length !== 0) {
            stack.push(nextBlockList);
        }
        var travelBlockList = [rootBlock];

        var iteration = 0;
        var current;
        while (stack.length !== 0) {
            current = stack.shift();
            iteration++;
            if (iteration > NUM_MAX_ITERATION) {
                console.log(ERROR_AB0002_INFINITE_LOOP);
                break;
            }
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                stack = DestructureFromBlockArray(stack, current);
            /** 배열이 아닐 때 */
            } else {
                var currBlock = current;
                travelBlockList.push(currBlock);
                var nextBlockList = current.getNextBlockList();
                stack.unshift(nextBlockList);
            }
        }

        var apiBlockJsonDataList = [];
        travelBlockList.forEach( (block, index) => {
            var nextBlockUUIDList = [ ...block.getNextBlockList().map(nextBlock => {
                    return nextBlock.getUUID();
                })
            ]
            apiBlockJsonDataList[index] = {
                UUID: block.getUUID()
                , prevBlockUUID: block.getPrevBlock() 
                                            ? block.getPrevBlock().getUUID() 
                                            : -1
                , nextBlockUUIDList
                , blockType: block.getBlockCodeLineType()
                , blockName: block.getBlockName()
                , blockOptionState: block.getState(STATE_optionState)
                , blockDepth: block.getDepth()
                , blockDirection: block.getDirection()
            }
        });
        return apiBlockJsonDataList;
    }

    BlockContainer.prototype.pushNowBlockList = function() {
        var apiBlockJsonDataList = this.makeAPIBlockMetadata();
        this.pushBlockHistoryStack(apiBlockJsonDataList);
    }

    BlockContainer.prototype.reRenderBlockList_fromMetadata = function(apiBlockJsonDataList) {
        var blockContainerThis = this;
        blockContainerThis.deleteContainerDom();
        blockContainerThis.makeContainerDom();

        /** metadata json을 기반으로 블럭 렌더링 */
        var createdBlockList = [];
        var createdBlock = null;
        apiBlockJsonDataList.forEach( (blockData, index) => {
            const { UUID, prevBlockUUID, nextBlockUUIDList
                     , blockType, blockName, blockOptionState, blockDepth, blockDirection } = blockData;
            createdBlock = blockContainerThis.createBlock(blockType, blockData);
            createdBlock.setUUID(UUID);
            createdBlock.setDepth(blockDepth);
            createdBlock.setDirection(blockDirection);
            createdBlock.setBlockName(blockName);
            createdBlock.setState({
                optionState: blockOptionState
            });
            createdBlock.setNextBlockUUIDList(nextBlockUUIDList);
            createdBlockList.push(createdBlock);
        });

        var _nextBlockUUIDList = [];
        createdBlockList.forEach((createdBlock,index) => {
            _nextBlockUUIDList = createdBlock.getNextBlockUUIDList();
            _nextBlockUUIDList.forEach(uuid => {

                createdBlockList.forEach(nextCreatedBlock => {
                    if (uuid == nextCreatedBlock.getUUID()) {
 
                        nextCreatedBlock.setPrevBlock(createdBlock);
                        createdBlock.addNextBlockList(nextCreatedBlock);
                        if (IsCanHaveIndentBlock(createdBlock.getBlockCodeLineType()) 
                            && nextCreatedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
                            createdBlock.setHolderBlock(nextCreatedBlock);
                        }
                    }           
                });
            });
        });

        this.setBlockList(createdBlockList);

        this.calculateDepthFromRootBlockAndSetDepth();
        this.reRenderBlockList(true);
        this.renderBlockLineNumberInfoDom(true);

    }

    BlockContainer.prototype.copyBlockList = function(travelBlockList, lastBlock, thisBlock) {
        var blockContainerThis = this;
        var apiBlockJsonDataList = [];
        var lastBlock_copyed;

        travelBlockList.map( (block, index) => {
            if (block.getUUID() == lastBlock.getUUID()) {
                lastBlock_copyed = block;
            }
            return block
        });

        travelBlockList.forEach( (block, index) => {
            var nextBlockUUIDList = [ ...block.getNextBlockList().map(nextBlock => {
                    return nextBlock.getUUID();
                })
            ]
       
            apiBlockJsonDataList[index] = {
                UUID: block.getUUID()
                , prevBlockUUID: block.getPrevBlock() 
                                            ? block.getPrevBlock().getUUID() 
                                            : -1
                , nextBlockUUIDList
                , blockType: block.getBlockCodeLineType()
                , blockName: block.getBlockName()
                , blockOptionState: block.getState(STATE_optionState)
                , blockDepth: block.getDepth()
                , blockDirection: block.getDirection()
            }

            if (index == 0) {
                apiBlockJsonDataList.prevBlockUUID = null;
            }

            if (block.getUUID() == lastBlock_copyed.getUUID()) {
                nextBlockUUIDList = []
            }
        });

        {
            var uuid_hable = [];
            apiBlockJsonDataList.forEach((blockData,index) => {
                const { UUID } = blockData;
                uuid_hable[UUID] = {
                    oldUUID: UUID
                    , newUUID: vpCommon.getUUID()
                }
            });

            var nextBlockUUIDList;
            apiBlockJsonDataList.forEach((blockData,index) => {
                var newNextBlockUUIDList = [];
                nextBlockUUIDList = blockData.nextBlockUUIDList;
                nextBlockUUIDList.forEach(uuid => {
                    if (uuid_hable[uuid] == undefined) {
                        return;
                    }
                    newNextBlockUUIDList.push(uuid_hable[uuid].newUUID)
                });

                blockData.nextBlockUUIDList = newNextBlockUUIDList;
                blockData.UUID = uuid_hable[blockData.UUID].newUUID;
            });
            uuid_hable = [];
        }

        var createdBlockList = [];
        var createdBlock = null;
        apiBlockJsonDataList.forEach( (blockData, index) => {
            const { UUID, prevBlockUUID, nextBlockUUIDList
                     , blockType, blockName, blockOptionState, blockDepth, blockDirection } = blockData;
            createdBlock = blockContainerThis.createBlock(blockType, blockData);
            createdBlock.setUUID(UUID);
            createdBlock.setDepth(blockDepth);
            createdBlock.setDirection(blockDirection);
            createdBlock.setBlockName(blockName);
            createdBlock.setState({
                optionState: blockOptionState
            });

 
            createdBlock.setNextBlockUUIDList(nextBlockUUIDList);
            createdBlockList.push(createdBlock);
        });
        
        var _nextBlockUUIDList = [];
        createdBlockList.forEach((createdBlock,index) => {
            _nextBlockUUIDList = createdBlock.getNextBlockUUIDList();
            _nextBlockUUIDList.forEach(uuid => {

                createdBlockList.forEach(nextCreatedBlock => {
                    if (uuid == nextCreatedBlock.getUUID()) {
                        nextCreatedBlock.setPrevBlock(createdBlock);
                        createdBlock.addNextBlockList(nextCreatedBlock);
                        if (IsCanHaveIndentBlock(createdBlock.getBlockCodeLineType()) 
                            && nextCreatedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
                            createdBlock.setHolderBlock(nextCreatedBlock);
                        }
                    }           
                });
            });
        });
        
        return createdBlockList;
    }

    BlockContainer.prototype.renderChildBlockListIndentAndGet = function() {

        var rootDepth = 0;
        var rootBlock = this.getRootBlock();
        if (rootBlock == null) {
            return [];
        }
   
        rootBlock.setDepth(rootDepth);

        //** root Block의 자식 Block depth */
        var childBlockList = rootBlock.getChildBlockList();
        childBlockList.forEach(async (block, index) => {

            var depth = block.calculateDepthAndGet();
            block.setDepth(depth);

            /** index 0일때 rootDepth를 계산*/
            if (index == 0) {
                rootDepth = depth;
                return;
            }
            /** index 1 이상 일때 */
            var indentPxNum = block.getIndentNumber();
            var numWidth = 0;
            /** TEXT 블럭과 그 외 일반 블럭의 WIDTH값을 다르게 함 */
            if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
                numWidth = NUM_TEXT_BLOCK_WIDTH - indentPxNum;
            } else {
                numWidth = NUM_BLOCK_MAX_WIDTH - indentPxNum;
            }

            var blockMainDom = block.getBlockMainDom();
            $(blockMainDom).css(STR_MARGIN_LEFT, indentPxNum + STR_PX);
            $(blockMainDom).css(STR_WIDTH, numWidth);
        });
        return childBlockList;
    }

    /** 
     * @async
     * Block editor에 존재하는 블럭들을 전부 다시 렌더링한다 
     */
    BlockContainer.prototype.reRenderBlockList = async function(isMetaData) {
        var blockContainerThis = this;
        var prevBlockList = this.getPrevBlockList();
        var blockList = this.renderChildBlockListIndentAndGet();
 
        /** metadata를 받아서 reRender */
        if (isMetaData == true) {
            blockContainerThis.deleteContainerDom();
            var containerDom = blockContainerThis.makeContainerDom();
        
            for await (var block of blockList) {
                new Promise( (resolve) => resolve( $(containerDom).append(block.getBlockMainDom())));
                block.bindEventAll();
            }
            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(containerDom);
            this.setPrevBlockList(blockList);
   
        } else if ( blockList < prevBlockList ) {
            // console.log(' blockList < prevBlockList');
            var deletedBlockList = RemoveSomeBlockAndGetBlockList(prevBlockList, blockList);
            deletedBlockList.forEach(block => {
               var blockMainDom = block.getBlockMainDom();
               $(blockMainDom).remove();
            });

            this.setPrevBlockList(blockList);

        } else if (blockList > prevBlockList) {

            // console.log('prevBlockList', prevBlockList);
            // console.log('blockList', blockList);

            var containerDom = this.getBlockContainerDom();
            var addedBlockList = RemoveSomeBlockAndGetBlockList(blockList, prevBlockList);
            var prevBlock = addedBlockList[0].getPrevBlock();
            if (prevBlock === null) {
               addedBlockList.forEach((addedBlock,index) => {
                   $(containerDom).append(addedBlock.getBlockMainDom() );
                   addedBlock.bindEventAll();
               });
           } else {
               addedBlockList.forEach(addedBlock => {
                   $( addedBlock.getBlockMainDom() ).insertAfter(prevBlock.getBlockMainDom());
                   addedBlock.bindEventAll();
                   prevBlock = addedBlock;
               });
           }
           this.setPrevBlockList(blockList);
     
        } else {
            blockContainerThis.deleteContainerDom();
            var containerDom = blockContainerThis.makeContainerDom();
            for await (var block of blockList) {
                new Promise( (resolve) => resolve( $(containerDom).append(block.getBlockMainDom())));
                block.bindEventAll();
            }

            $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(containerDom);
            this.setPrevBlockList(blockList);
        }
    }

     /** Block 앞에 line number를 정렬
      * isAsc true면 오름차순 정렬
     */
     BlockContainer.prototype.renderBlockLineNumberInfoDom = async function(isAsc) {

        var rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return;
        }

        var blockChildList = rootBlock.getChildBlockList();
        // var nodeBlockList = this.getNodeBlockList();
        var nodeBlockList = [];
        var minusIndex = 0;
        blockChildList.forEach((block, index) => {
            if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE) {
                nodeBlockList.push(block);
            }

            if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE ) {

            } else if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
                var numberPx = -(NUM_DEFAULT_POS_X - 3);
                var $blockLineNumberInfoDom = $(block.getBlockLineNumberInfoDom());
                $blockLineNumberInfoDom.css( STR_LEFT, numberPx + STR_PX );
            } else {
                var $blockLineNumberInfoDom = $(block.getBlockLineNumberInfoDom());
                $blockLineNumberInfoDom.css(STR_OPACITY,0);
                $(block.getBlockDepthInfoDom()).css(STR_OPACITY,1);
            }

            if (block.getDepth() == 0) {
                $(block.getBlockDepthInfoDom()).css(STR_OPACITY,0);
            }
        });
        var blockAmount = nodeBlockList.length;
        nodeBlockList.forEach(async (block, index) => {
            var index = index + 1;
            if (block.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.HOLDER) {
                var numberPx = -(NUM_DEFAULT_POS_X - 3);

                var $blockLineNumberInfoDom = $(block.getBlockLineNumberInfoDom());
                $blockLineNumberInfoDom.css( STR_LEFT, numberPx + STR_PX );
                var blockLineNumber = 0;

                /** Line number 오름차순 정렬의 경우 */
                if (isAsc == true) {
                    $blockLineNumberInfoDom.css(STR_COLOR, '#828282');
                    blockLineNumber = index - minusIndex;
                    block.setBlockNumber(blockLineNumber);
                /** 처음 생성한 Line number를 그대로 보여줄 경우 */
                } else {
                    blockLineNumber = block.getBlockNumber();
                    block.setBlockNumber(blockLineNumber);
                }
           
                if (blockLineNumber >= NUM_MAX_BLOCK_NUMBER) {
                    blockLineNumber = NUM_MAX_BLOCK_NUMBER;
                }

                // var prefixNumInfo = this.makeBlockLineNumberstr( blockAmount, blockLineNumber );
                // this.makeBlockLineNumberInfoDom(block);
                // $blockLineNumberInfoDom = $(block.getBlockLineNumberInfoDom());
                // $blockLineNumberInfoDom.find('.vp-block-prefixnum-info').text(prefixNumInfo);
                // $blockLineNumberInfoDom.find('.vp-block-linenumber-info').text(blockLineNumber);
                $blockLineNumberInfoDom.text(block.getBlockNumber());
          
            } else {
                minusIndex++;
            }
        });
    }
    
    BlockContainer.prototype.reRenderAllBlock = function() {
        this.calculateDepthFromRootBlockAndSetDepth();
        this.reRenderBlockList();
        this.renderBlockLineNumberInfoDom();
    }
    
    BlockContainer.prototype.reRenderAllBlock_asc = function() {
        this.calculateDepthFromRootBlockAndSetDepth();
        this.reRenderBlockList();
        this.renderBlockLineNumberInfoDom(true);
    }

    /** line number 앞에 prefix로 0 붙여주는 메소드 */
    BlockContainer.prototype.makeBlockLineNumberstr = function(blockAmount, blockLineNumber) {
        var prefixNuminfo = '';
        if ( blockAmount >= 1000 ) {
            if ( blockLineNumber >= 1000 ){
    
            } else if ( blockLineNumber >= 100 ) {
                prefixNuminfo += '0';
            } else if ( blockLineNumber >= 10 ) {
                prefixNuminfo += '00';
            } else {
                prefixNuminfo += '000';
            }
        } else if ( blockAmount >= 100 ) {
            if ( blockLineNumber >= 1000 ){
    
            } else if ( blockLineNumber >= 100 ) {
          
            } else if ( blockLineNumber >= 10 ) {
                prefixNuminfo += '0';
            } else {
                prefixNuminfo += '00';
            }
        } else if ( blockAmount >= 10) {
            if ( blockLineNumber >= 10) {

            } else {
                prefixNuminfo += `0`;
            }
        } else {
    
        }
        return prefixNuminfo;
    }

    /**
     * @param {BLOCK} checkBlock 
     */
    BlockContainer.prototype.getRootToLastBottomBlock = function() {
        var rootBlock = this.getRootBlock();
        return this.getLastBottomBlock(rootBlock);
    }

    /**
     * @param {BLOCK} thisBlock 
     */
    BlockContainer.prototype.getLastBottomBlock = function(thisBlock) {
        var childBlockList = thisBlock.getChildBlockList();
        var childBlockList_down = childBlockList.filter(childBlock => {
            if (childBlock.getDirection() == BLOCK_DIRECTION.DOWN) {
                return true;
            } else {
                return false;
            }
        })
        var current = childBlockList_down[childBlockList_down.length-1];
        return current;
    }
    BlockContainer.prototype.dragBlock = function(isBlock, thisBlock, shadowBlock, selectedBlock, selectedBlockDirection, currCursorX, currCursorY) {
        var blockContainerThis = this;
        /** 블록 전체를 돌면서 drag하는 Block과 Editor위에 생성된 블록들과 충돌 작용  */
        var blockList = blockContainerThis.getBlockList();
        var nodeBlockList = blockContainerThis.getNodeBlockList();
        var blockList = blockContainerThis.getBlockList();
            blockList.forEach( async (block) => {

                if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
                    return;
                }

                if (isBlock == true) {
                    /** 자기 자신인 블럭과는 충돌 금지 
                         *  혹은 자신의 하위 블럭과도 충돌 금지
                    */
                    // if ( thisBlock.getUUID() == block.getUUID()
                    //     || block.getIsNowMoved() == true ) {
                    //     return;
                    // }
                    if ( thisBlock.getUUID() == block.getUUID() ) {
                        return;
                    }
                    // var childLowerDepthBlockList = block.getChildLowerDepthBlockList();
                    // var isChildBlock = childLowerDepthBlockList.some(childBlock => {
                    //     if (thisBlock.getUUID() == childBlock.getUUID()) {
                    //         return true;
                    //     }
                    // });
                    // if (isChildBlock == true) {
                    //     return;
                    // }

                    if ( thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE
                        || thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT ) {
                        var isNodeBlock = nodeBlockList.some((nodeBlock,index) => {
                            nodeBlock.getChildLowerDepthBlockList();
                                    
                            if (nodeBlock.getDirection() != BLOCK_DIRECTION.ROOT
                                && nodeBlock.getLastChildBlock().getUUID() == block.getUUID()) {
                                    
                                $( block.getBlockMainDom() ).css(STR_DISPLAY, STR_FLEX);
                                        
                                var blockLeftHolderDom = block.getBlockLeftHolderDom();
                                $(blockLeftHolderDom).css(STR_DISPLAY, STR_BLOCK);
                                return true;
                            } else {
                                return false;
                            }
                        });
                        if (isNodeBlock == false) {
                            return;
                        }
                    }
                }
                /** 충돌할 block의 x,y, width, height를 가져온다 */
                var { x: blockX, 
                      y: blockY, 
                      width: blockWidth, 
                      height: blockHeight } = block.getBlockMainDomPosition();

                /** 블럭 충돌에서 벗어나는 로직 */
                var blockLeftHolderHeight = block.getTempBlockLeftHolderHeight();
                if ( (blockX > currCursorX 
                      || currCursorX > (blockX + blockWidth)
                      || blockY  > currCursorY 
                      || currCursorY > (blockY + blockHeight + blockHeight + blockHeight + blockLeftHolderHeight) ) ) {
                    block.renderBlockHolderShadow(STR_NONE);
                
                }

                /** 블럭 충돌 left holder shadow 생성 로직 */
                if ( blockX < currCursorX
                    && currCursorX < (blockX + blockWidth)
                    && blockY  < currCursorY
                    && currCursorY < (blockY + blockHeight + blockHeight + blockLeftHolderHeight) ) {     
                    block.renderBlockHolderShadow(STR_BLOCK);

                    var holderBlock = block.getHolderBlock();
                    if ( holderBlock != null ) {
                         block.renderBlockLeftHolderHeight();
                    }
                }

                /** 블럭 충돌 로직 */  
                if ( blockX < currCursorX
                        && currCursorX < (blockX + blockWidth + blockWidth)
                        && blockY  < currCursorY
                        && currCursorY < (blockY + blockHeight  + blockHeight) ) { 

                    var holderBlock = block.getHolderBlock();
                    if ( holderBlock != null ) {
                        block.renderBlockLeftHolderHeight();
                    }

                    /** 충돌시 direction 설정
                     * direction은 DOWN,  INDENT
                     */
                    var holderBlock = block.getHolderBlock();
                    if ( holderBlock != null ) {
                        selectedBlockDirection = BLOCK_DIRECTION.INDENT;
                    } else {
                        selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                    }

                    block.makeShadowDomList( shadowBlock, selectedBlockDirection);
                } else {
                    /** shadow 블록 생성하는 로직
                     * css class로 마크된 block을 selectedBlock에 저장 한다
                     */
                    if ( $(shadowBlock.getBlockMainDom()).hasClass(VP_CLASS_SELECTED_SHADOWBLOCK) ) {
                        selectedBlock = shadowBlock.getSelectBlock();
                    }

                }
            });

        return { 
            selectedBlock, 
            selectedBlockDirection
        };
    }

    BlockContainer.prototype.stopDragBlock = function(isBlock, thisBlock) {
        var blockContainerThis = this;

        if (isBlock == true) {
            blockContainerThis.reRenderAllBlock();       
            thisBlock.renderEditorScrollTop();

            // var nodeBlock = blockContainerThis.findNodeBlock(thisBlock);
            // if (nodeBlock.getIsNodeBlockToggled() == true) {
            //     nodeBlock.setIsNodeBlockToggled(false);
            //     $(nodeBlock.getBlockMainDom()).css('box-shadow', STR_NONE);
        
            //     var childLowerDepthBlockList = nodeBlock.getChildLowerDepthBlockList();
            //     childLowerDepthBlockList.forEach( (block,index) => {
            //         if (index != 0) {
            //             if (block.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.HOLDER) {
            //                 $(block.getBlockMainDom()).addClass('vp-apiblock-style-display-flex');
            //                 $(block.getBlockMainDom()).removeClass('vp-apiblock-style-display-none');
            //             }
            //         }
            //     });
            // }

        } else {
            blockContainerThis.reRenderAllBlock_asc();
            blockContainerThis.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BUTTONS);

            var nodeBlock = blockContainerThis.findNodeBlock(thisBlock);
            nodeBlock.setIsNodeBlockToggled(false);
            $(nodeBlock.getBlockMainDom()).css('box-shadow', STR_NONE);
    
            var childLowerDepthBlockList = nodeBlock.getChildLowerDepthBlockList();
            childLowerDepthBlockList.forEach( (block,index) => {
                if (index != 0) {
                    if (block.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.HOLDER) {
                        $(block.getBlockMainDom()).addClass('vp-apiblock-style-display-flex');
                        $(block.getBlockMainDom()).removeClass('vp-apiblock-style-display-none');
                    }
                }
            });
        }

        /** 모든 0 Depth Block 한칸 띄우기
         *  모든 Block border color 리셋
         *  모든 Block에서 생성된 shadow 지우기
         */
        var blockList = blockContainerThis.getBlockList();
        blockList.forEach(block => {
            block.renderBlockHolderShadow(STR_NONE);
            block.renderSelectedBlockColor(false);
            $(block.getBlockMainDom()).find(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SUB_BTN_CONTAINER).remove();
        });

        /** 옵션 페이지 다시 오픈 */
        blockContainerThis.setSelectedBlock(thisBlock);
        blockContainerThis.renderBlockOptionTab();

        /** 서브 버튼 생성 */
        thisBlock.createSubButton();
        /** 자식 하위 Depth Block Border 색칠 */
        thisBlock.renderMyColor(true);
    }

    /** 블럭 이동시 모든 블럭의 left shadow 계산 */
    BlockContainer.prototype.reLoadBlockListLeftHolderHeight = function() {
        const blockContainerThis = this;
        const blockList = blockContainerThis.getBlockList();
        blockList.forEach(block => {
            const holderBlock = block.getHolderBlock();
            if ( holderBlock != null ) {
                block.calculateLeftHolderHeightAndSet();
                const distance = block.getTempBlockLeftHolderHeight();
                $(block.getBlockLeftHolderDom()).css(STR_HEIGHT, distance);
            } 
        });
    }

    /**
     *  옵션 페이지를 렌더링하는 메소드
     */
    BlockContainer.prototype.renderBlockOptionTab = function() {
        var selectedBlock = this.getSelectedBlock();
        // console.log('selectedBlock',selectedBlock);
        if(selectedBlock) {
            selectedBlock.resetOptionPage();
            selectedBlock.renderOptionPage();
        }
    }

    /* 현재 this 블럭이 속한 node 블럭을 찾아서 return */
    BlockContainer.prototype.findNodeBlock = function(thisBlock) {
        var blockContainerThis = this;
        var nodeBlockList = blockContainerThis.getNodeBlockList();
        var selectedBlock = blockContainerThis.getSelectedBlock() || thisBlock;
        nodeBlockList.some(nodeBlock => {
            var childLowerDepthBlockList = nodeBlock.getChildLowerDepthBlockList();
            childLowerDepthBlockList.push(nodeBlock);
            childLowerDepthBlockList.some(block => {
                if (block.getUUID() == selectedBlock.getUUID()) {
                    selectedBlock = nodeBlock;
                    return true;
                }
            });
        });
        return selectedBlock;
    }

    BlockContainer.prototype.makeNodeBlock = function() {
        var blockContainerThis = this;
        var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.NODE);
        var length = blockContainerThis.getNodeBlockNumber();
        newBlock.setState({
            [STATE_codeLine]: `Node ${length}`
        });
        newBlock.setIsNodeBlockToggled(true);
        $(newBlock.getBlockMainDom()).css('box-shadow','0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)');
        $(`#vp_apiblock_nodeblock_${newBlock.getUUID()}`).text(`Node ${length}`);
        return newBlock;
    }

    BlockContainer.prototype.makeTextBlock = function() {
        var blockContainerThis = this;
        var newBlock = blockContainerThis.createBlock(BLOCK_CODELINE_TYPE.TEXT);
        newBlock.setState({
            [STATE_codeLine]: ``
        });
        newBlock.writeCode('');
        return newBlock;
    }

    BlockContainer.prototype.makeShadowBlock = function(blockContainerThis, blockCodeLineType, 
                                                        shadowChildBlockDomList, thisBlock) {
        var shadowBlock = new ShadowBlock(blockContainerThis, blockCodeLineType, 
                                            shadowChildBlockDomList, thisBlock);
        var $shadowBlockMainDom = $(shadowBlock.getBlockMainDom());
        $shadowBlockMainDom.css(STR_DISPLAY,STR_NONE);

        var containerDom = blockContainerThis.getBlockContainerDom();
        $(containerDom).append(shadowBlock.getBlockMainDom());

        return shadowBlock;
    }

    BlockContainer.prototype.deleteContainerDom = function() {
        var containerDom = this.getBlockContainerDom();
        $(containerDom).empty();
        $(containerDom).remove();
        $(VP_CLASS_PREFIX + VP_CLASS_BLOCK_CONTAINER).remove();
    }

    BlockContainer.prototype.reNewContainerDom = function() {
        var blockContainerThis = this;
        blockContainerThis.deleteContainerDom();
        var containerDom = blockContainerThis.makeContainerDom();
        $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(containerDom);
        return containerDom;
    }

    BlockContainer.prototype.makeContainerDom = function() {
        var blockContainerThis = this;
        var containerDom = document.createElement(STR_DIV);
        containerDom.classList.add(VP_CLASS_BLOCK_CONTAINER);
        this.setBlockContainerDom(containerDom);

        $(containerDom).css(STR_TOP, NUM_DEFAULT_POS_Y + STR_PX);
        $(containerDom).css(STR_LEFT, NUM_DEFAULT_POS_X + STR_PX);

        var nodePlusButtonContainer = $(` <div id="vp_apiblock_board_node_plus_button_container" 
                                                class="vp-apiblock-style-flex-row">
                                            </div>`);

        var nodePlusButton = $(`<div id="vp_apiblock_board_node_plus_button"
                                    class="vp-apiblock-option-plus-button"> 
                                    + Node
                                </div>`);
        var textPlusButton = $(`<div id="vp_apiblock_board_text_plus_button"
                                    class="vp-apiblock-option-plus-button"
                                    style="margin-left: 10px;"> 
                                    + Text
                                </div>`);
        nodePlusButtonContainer.append(nodePlusButton);
        nodePlusButtonContainer.append(textPlusButton);

        $(nodePlusButton).off(STR_CLICK);
        $(nodePlusButton).click(function() {
            var newBlock;
            if (blockContainerThis.getBlockList().length == 0) {
                newBlock = blockContainerThis.makeNodeBlock();
                newBlock.setDirection(BLOCK_DIRECTION.ROOT);

                blockContainerThis.reNewContainerDom();
          
            } else {
                newBlock = blockContainerThis.makeNodeBlock();
                var rootBlock = blockContainerThis.getRootBlock();
                var childBlockList = rootBlock.getChildBlockList();
                childBlockList[childBlockList.length-1].appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
    
                newBlock.renderEditorScrollTop();
            }

            blockContainerThis.reRenderAllBlock_asc();
            blockContainerThis.setSelectedBlock(newBlock);
            blockContainerThis.renderBlockOptionTab();

            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SUB_BTN_CONTAINER)).remove();

            var blockList = blockContainerThis.getBlockList();
            blockList.forEach(block => {
                block.renderSelectedBlockColor(false);
            });

            newBlock.createSubButton();
            newBlock.renderSelectedBlockColor(true);
            newBlock.renderSelectedMainBlockBorderColor();
        });

        $(textPlusButton).off(STR_CLICK);
        $(textPlusButton).click(function() {
            api_listInit(blockContainerThis, BLOCK_CODELINE_TYPE.TEXT);
        });

        var blockList = blockContainerThis.getBlockList();
        blockList.forEach(block => {
            block.renderSelectedBlockColor(false);
        });

        $(containerDom).append(nodePlusButtonContainer);
        return containerDom;
    }   

    BlockContainer.prototype.makeBlockDom = function(block, isFirst) {
        /** 이동하는 block과 동일한 모양의 html tag 생성*/
        var blockMainDom = RenderBlockMainDom(block);

        /** 이동하는 block의 header 생성 */
        const mainInnerDom = RenderBlockMainInnerDom(block);
        const mainHeaderDom = RenderBlockMainHeaderDom(block);

        $(mainInnerDom).append(mainHeaderDom);
        $(blockMainDom).append(mainInnerDom);

        var blockLeftHolderDom = RenderBlockLeftHolderDom();
           
        blockMainDom = RenderHTMLDomColor(block, blockMainDom);
        blockLeftHolderDom = RenderHTMLDomColor(block, blockLeftHolderDom);
        const blockLeftHolderHeight = block.getTempBlockLeftHolderHeight();
        $(blockLeftHolderDom).css(STR_HEIGHT,`${blockLeftHolderHeight}${STR_PX}`);
        $(blockMainDom).append(blockLeftHolderDom);

        if (isFirst == true) {
            block.setBlockInnerDom(mainInnerDom);
            block.setBlockHeaderDom(mainHeaderDom);
            block.setBlockLeftHolderDom(blockLeftHolderDom);
        } else {
            /** 이동하는 block의 처음 block의 width 값 계산 */
            const rect = $(`.vp-block-${block.getUUID()}`)[0].getBoundingClientRect();
            $(blockMainDom).css(STR_WIDTH, rect.width);
        }

        return blockMainDom;
    }

    BlockContainer.prototype.makeBlockLineNumberInfoDom = function(block) {
        var blockLineNumberInfoDom = document.createElement(STR_SPAN);
        blockLineNumberInfoDom.classList.add(VP_CLASS_BLOCK_NUM_INFO);
        $(blockLineNumberInfoDom).append($(`<span class='vp-block-prefixnum-info'>
                                            </span>`));
        $(blockLineNumberInfoDom).append($(`<span class='vp-block-linenumber-info'>
                                            </span>`));                                          
        block.setBlockLineNumberInfoDom(blockLineNumberInfoDom);   

        var blockMainDom = block.getBlockMainDom();
        $(blockMainDom).append(blockLineNumberInfoDom);

        return blockMainDom;
    }

    BlockContainer.prototype.openOptionPopup = function() {
        this.setIsOptionPageOpen(true);
        // var vpOptionPageRectWidth = this.getOptionPageWidth() || NUM_OPTION_PAGE_WIDTH;
        // $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_DISPLAY, STR_BLOCK);
        // $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_RIGHT, 0);
        // $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, vpOptionPageRectWidth);
       
        
        // var mainPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MAIN))[0].getBoundingClientRect();
        // var buttonsPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS))[0].getBoundingClientRect();
    
        // var mainPageRectWidth = mainPageRect.width; 
        // var buttonsPageRectWidth = buttonsPageRect.width; 
        // var boardPageRectWidth = mainPageRectWidth - vpOptionPageRectWidth - buttonsPageRectWidth;
        // $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).css(STR_WIDTH, boardPageRectWidth);
    }

    BlockContainer.prototype.closeOptionPopup = function(block) {
        if (block) {
            this.setSelectedBlock(block);
        }
    }


    BlockContainer.prototype.resizeOptionPopup = function() {
        var optionPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB))[0].getBoundingClientRect();
        var mainPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MAIN))[0].getBoundingClientRect();
        var buttonsPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS))[0].getBoundingClientRect();
        var mainPageRectWidth = mainPageRect.width; 
        var buttonsPageRectWidth = buttonsPageRect.width; 
        var optionPageRectWidth = optionPageRect.width;
        var boardPageRectWidth = mainPageRectWidth - optionPageRectWidth - buttonsPageRectWidth;

        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_MAX_WIDTH, mainPageRectWidth - buttonsPageRectWidth - 20);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).css(STR_WIDTH, boardPageRectWidth );
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, optionPageRectWidth - 20);
        this.setOptionPageWidth(optionPageRectWidth - 20); 
    }

    BlockContainer.prototype.resizeOptionPopup_wrapper = function() {
        // console.log('resizeOptionPopup_wrapper');
        var mainPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MAIN))[0].getBoundingClientRect();
        var buttonsPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS))[0].getBoundingClientRect();
        var boardPageRect = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD))[0].getBoundingClientRect();

        var mainPageRectWidth = mainPageRect.width; 
        var buttonsPageRectWidth = 140; 
        var boardPageRectWidth = 350; 

        var optionPageRectWidth = mainPageRectWidth - boardPageRectWidth - buttonsPageRectWidth - 10;
        // this.setOptionPageWidth(optionPageRectWidth);

        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, optionPageRectWidth);
        // if (optionPageRectWidth < NUM_OPTION_PAGE_WIDTH) {
        //     optionPageRectWidth = NUM_OPTION_PAGE_WIDTH;
        // }
    }

    BlockContainer.prototype.resetBlockList = function() {
        /** 
         *  Block color 리셋
         */ 
        const blockContainerThis = this;
        const blockList = blockContainerThis.getBlockList();
        for (var block of blockList) {
            block.renderSelectedBlockColor(false);
            $(block.getBlockMainDom()).css(STR_BORDER, '2px solid transparent');
        }

        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_BLOCK_SUB_BTN_CONTAINER)).remove();
        
        const nodeBlockList = blockContainerThis.getNodeBlockList();
        nodeBlockList.forEach(block => {
            const blockUUID = block.getUUID();
            $(`.vp-apiblock-nodeblock-input-${blockUUID}`).css(STR_DISPLAY, STR_NONE);
            $(`.vp-apiblock-nodeblock-${blockUUID}`).css(STR_DISPLAY, STR_BLOCK);
            block.setIsNodeBlockInput(false);
        });
    }

    /** importPackage의 generateCode 이전에 실행할 prefix code
     *  @param {boolean} isClicked true면 클릭 이벤트로 코드 실행
     */
    BlockContainer.prototype.generateCode = function(isClicked) {
        var importPackageThis = this.getImportPackageThis();
        importPackageThis.generateCode(true, true, isClicked);
    }

    BlockContainer.prototype.makeCode = function(thisBlock) {
        var codeLine = '';
        if (thisBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT){
            thisBlock.getImportPakage().generateCode(true, true);
            return;
        }

        var childLowerDepthBlockList = thisBlock.getChildLowerDepthBlockList();
        var rootDepth = thisBlock.getDepth();
        childLowerDepthBlockList.some( ( block,index ) => {
            if ( block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER ) {
                return false;
            }

            var indentString = block.getIndentString(rootDepth);

            if ( block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.API ) {
                var apiCodeLine = block.setCodeLineAndGet(indentString, true);
                if (apiCodeLine.indexOf('BREAK_RUN') != -1 || apiCodeLine == '') {
                    codeLine = 'BREAK_RUN';
                    return true;
                } else {
                    codeLine += apiCodeLine;
                }
            } else {
                codeLine += block.setCodeLineAndGet(indentString, false);
            }
            codeLine += STR_KEYWORD_NEW_LINE;
        });
        vpCommon.setIsAPIListRunCode(true);
        return codeLine;
    }

    BlockContainer.prototype.previewCode = function(thisBlock) {
        vpCommon.setIsAPIListRunCode(false);

        var rootDepth = thisBlock.getDepth();
        var codeLine = ``;
        // var codeLine = `# [Visual Python] Node ${thisBlock.getBlockNumber()} : ${thisBlock.getState(STATE_codeLine)}`;
        var childLowerDepthBlockList = thisBlock.getChildLowerDepthBlockList();
        childLowerDepthBlockList.forEach( ( block ) => {
            if ( block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER ) {
                return;
            }

            var indentString = block.getIndentString(rootDepth);
            var thisCodeLine =  block.setCodeLineAndGet(indentString, false);
            /** api list validation 걸릴 때 BREAK_RUN을 반환*/
            if (thisCodeLine.indexOf('BREAK_RUN') != -1) {
                /** 그래서 BREAK_RUN을 replace함수로 제거 */
                thisCodeLine = thisCodeLine.replace('BREAK_RUN','');
            }
            codeLine += thisCodeLine;
            codeLine += STR_KEYWORD_NEW_LINE;
        });

        vpCommon.setIsAPIListRunCode(true);
        return codeLine;
    }

    /**
     * block의 depth를 계산하고 block 앞에 depth 를 보여주는 함수
     */
    BlockContainer.prototype.calculateDepthFromRootBlockAndSetDepth = function() {
        const rootBlock = this.getRootBlock();
        if (!rootBlock) {
            return;
        }

        const getChildBlockList = rootBlock.getChildBlockList();
        getChildBlockList.forEach((block) => {
            if (block.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.HOLDER) {
                return;
            }
            var depth = block.calculateDepthAndGet();
            var blockDepthInfoDom = block.getBlockDepthInfoDom();
            blockDepthInfoDom.text(depth);
        });
    }



    /**  LoadedVariableList  예제
        0:
        varName: "cam"
        varType: "DataFrame"
    */

    BlockContainer.prototype.setKernelLoadedVariableList = function(loadedVariableList) {
        this.loadedVariableList = loadedVariableList;
    }

    /** varName varType를 Array로 다 가져오기*/
    BlockContainer.prototype.getKernelLoadedVariableList = function() {
        return this.loadedVariableList;
    }

    /** varName만 Array로 가져오기*/
    BlockContainer.prototype.getKernelLoadedVariableNameList = function() {
        return this.loadedVariableList.map(varData => {
            return varData.varName;
        });
    }

    /** metadata init */
    BlockContainer.prototype.setAPIBlockMetadataHandler = function() {  
        var importPackageThis = this.getImportPackageThis();
        this.setMetahandler(importPackageThis.funcID);
        this.mdHandler.generateMetadata(importPackageThis);  
        this.mdHandler.metadata.apiblockList = [];
    }

    /** metadata set */
    BlockContainer.prototype.setAPIBlockMetadata = function() {  
        var importPackageThis = this.getImportPackageThis();  
        var apiBlockJsonDataList = this.makeAPIBlockMetadata();  
        var encoded_apiBlockJsonDataList = encodeURIComponent(JSON.stringify(apiBlockJsonDataList));
        
        /** API BLOCK container가 가지고 있는 metadata 
         *  이 데이터는 API Block가 metadata를 핸들링하기 위해 존재
         */
        this.mdHandler.metadata.apiblockList = encoded_apiBlockJsonDataList;
        /** importPackage가 가지고 있는 metadata 
         *  이 데이터는 #vp_saveOn 버튼을 누를시 vpNote로 간다.
        */
        importPackageThis.metadata = this.mdHandler.metadata;        
    }

    /** metadata 로드 */
    BlockContainer.prototype.loadAPIBlockMetadata = function(loadedMetadata) {
        if (loadedMetadata) {
            var importPackageThis = this.getImportPackageThis(); 
            var decodedMetadata = decodeURIComponent(loadedMetadata.apiblockList);
            var parsedDecodedMetadata = JSON.parse(decodedMetadata);

            this.mdHandler.metadata = loadedMetadata;
            this.mdHandler.metadata.apiblockList = parsedDecodedMetadata;
            importPackageThis.metadata = this.mdHandler.metadata;  

            this.reRenderBlockList_fromMetadata(parsedDecodedMetadata);   
        } 
    }

    /** metadata 세이브 */
    BlockContainer.prototype.saveAPIBlockMetadata = function(isMessage = false) {  
        var apiBlockJsonDataList = this.makeAPIBlockMetadata();  
        var importPackageThis = this.getImportPackageThis();  
        var encoded_apiBlockJsonDataList = encodeURIComponent(JSON.stringify(apiBlockJsonDataList));
        this.mdHandler.metadata.apiblockList = encoded_apiBlockJsonDataList;

        importPackageThis.metadata = this.mdHandler.metadata;  
        this.mdHandler.saveMetadata(this.mdHandler.metadata);
    }

    //
    BlockContainer.prototype.setOptionDom = function(UUID, type, blockOptionPageDom_new) {
        if (this.domPool.get(UUID)) {
            if (type == BLOCK_CODELINE_TYPE.TEXT || type == BLOCK_CODELINE_TYPE.API) {
                const blockOptionPageDom_old = this.domPool.get(UUID);
                $(blockOptionPageDom_old).css(STR_DISPLAY, STR_NONE);
            } else {
                const blockOptionPageDom_old = this.domPool.get(UUID);
                $(blockOptionPageDom_old).remove();
            }
        }
        this.domPool.set(UUID, blockOptionPageDom_new);
    }

    BlockContainer.prototype.getOptionDom = function(UUID) {
        const blockOptionPageDom = this.domPool.get(UUID);
        return blockOptionPageDom;

    }
    
    BlockContainer.prototype.getOptionDomPool = function(blockOptionPageDom_new) {
        for (const blockOptionPageDom_old of this.domPool.values()) {
            $(blockOptionPageDom_old).css({
                display: 'none'
            });
        }
        $(blockOptionPageDom_new).css({
            display: 'block'
        });
    }

    BlockContainer.prototype.getBoardPage_$ = function() {
        var $boardPage = $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD));
        return $boardPage;
    }


    return BlockContainer;
});
