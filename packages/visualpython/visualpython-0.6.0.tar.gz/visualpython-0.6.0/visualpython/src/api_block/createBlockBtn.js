define([

    './api.js'
    , './constData.js'
    , './blockRenderer.js'
], function ( api, constData, blockRenderer ) {
    const { ChangeOldToNewState
            , FindStateValue
            , MapTypeToName } = api;
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION

            , VP_CLASS_PREFIX
            , VP_CLASS_APIBLOCK_MAIN    
            , VP_CLASS_APIBLOCK_BOARD } = constData;  

    const { RenderHTMLDomColor } = blockRenderer;
 

    var CreateBlockBtn = function(blockContainerThis, type) { 
        this.blockContainerThis = blockContainerThis;
        this.state = {
            type
            , name: ''
        }
        this.rootDomElement = null;

        this.setState({
            name: MapTypeToName(type)
        });
        this.render();
        this.bindBtnDragEvent();
    }

    CreateBlockBtn.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }


    CreateBlockBtn.prototype.getBlockName = function() {
        return this.state.name;
    }

    CreateBlockBtn.prototype.setBlockName = function(name) {
        this.setState({
            name
        });
    }
    CreateBlockBtn.prototype.getBlockCodeLineType = function() {
        return this.state.type;
    }






    CreateBlockBtn.prototype.getBlockMainDom = function() {
        return this.rootDomElement;
    }

    CreateBlockBtn.prototype.setBlockMainDom = function(rootDomElement) {
        this.rootDomElement = rootDomElement;
    }
    CreateBlockBtn.prototype.getBlockMainDomPosition = function() {
        var rootDom = this.getBlockMainDom();
        var clientRect = $(rootDom)[0].getBoundingClientRect();
        return clientRect;
    }







    // ** Block state 관련 메소드들 */
    CreateBlockBtn.prototype.setState = function(newState) {
        this.state = ChangeOldToNewState(this.state, newState);
        this.consoleState();
    }
    /**
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    CreateBlockBtn.prototype.getState = function(stateKeyName) {
        return FindStateValue(this.state, stateKeyName);
    }
    CreateBlockBtn.prototype.getStateAll = function() {
        return this.state;
    }
    CreateBlockBtn.prototype.consoleState = function() {
        // console.log(this.state);
    }






    CreateBlockBtn.prototype.render = function() {
        var blockContainer = null;
        var rootDomElement = $(`<div class='vp-apiblock-tab-navigation-node-block-body-btn'>
                                    <span class='vp-block-name'>
                                        ${this.getBlockName()}
                                    </span>
                                </div>`);

        this.setBlockMainDom(rootDomElement);
        rootDomElement = RenderHTMLDomColor(this, rootDomElement);

        var blockCodeType = this.getBlockCodeLineType();
        if (blockCodeType == BLOCK_CODELINE_TYPE.CLASS 
            || blockCodeType == BLOCK_CODELINE_TYPE.DEF) {
            blockContainer = $(`.vp-apiblock-tab-navigation-node-subblock-1-body-inner`);
    
        } else if (blockCodeType == BLOCK_CODELINE_TYPE.IF 
            || blockCodeType == BLOCK_CODELINE_TYPE.FOR
            || blockCodeType == BLOCK_CODELINE_TYPE.WHILE 
            || blockCodeType == BLOCK_CODELINE_TYPE.TRY
            || blockCodeType == BLOCK_CODELINE_TYPE.CONTINUE
            || blockCodeType == BLOCK_CODELINE_TYPE.BREAK
            || blockCodeType == BLOCK_CODELINE_TYPE.PASS
            || blockCodeType == BLOCK_CODELINE_TYPE.RETURN) {
            blockContainer = $(`.vp-apiblock-tab-navigation-node-subblock-2-body-inner`);
  
        }  else  {
            blockContainer = $(`.vp-apiblock-tab-navigation-node-subblock-3-body-inner`);
        }
        blockContainer.append(rootDomElement);
    }

    CreateBlockBtn.prototype.bindBtnDragEvent = function() {
        var thisBlockBtn = this;
        var rootDom = this.getBlockMainDom();
        var blockContainerThis = this.getBlockContainerThis();
        var blockCodeLineType = this.getBlockCodeLineType();

        var currCursorX = 0;
        var currCursorY = 0;
        var newPointX = 0;
        var newPointY = 0;

        var selectedBlockDirection = null;
        var shadowBlock = null;
        var newBlock = null;
        var rootBlock =  null; 

        var thisBlockBtnWidth = 0;
        $(rootDom).draggable({ 
            appendTo: VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MAIN,
            containment: VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MAIN,
            cursor: 'move', 
            helper: 'clone',
            start: function(event, ui) {

                rootBlock = blockContainerThis.getRootBlock();
                if (rootBlock) {
                    /** shadow 블럭 생성 */
                    shadowBlock = blockContainerThis.makeShadowBlock( blockContainerThis, blockCodeLineType, []);
                }

                /** height 길이 결정 */
                blockContainerThis.reLoadBlockListLeftHolderHeight();
                ({ width: thisBlockBtnWidth } = thisBlockBtn.getBlockMainDomPosition());
            },
            drag: async function(event, ui) {  
       
                currCursorX = event.clientX; 
                currCursorY = event.clientY; 

                /** 만약  아래 로직에서 + thisBlockWidth + 10이 없다면 마우스 커서 오른쪽으로 이동 됨*/
                newPointX = currCursorX - $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).offset().left  + thisBlockBtnWidth + 50 ;
                newPointY = currCursorY - $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).offset().top + 50 ;

                /** drag Block 생성 버튼 마우스 커서 왼쪽 위로 이동 구현 */
                ui.position = {
                    top: newPointY,
                    left: newPointX
                };

                ({ selectedBlock, selectedBlockDirection } = blockContainerThis.dragBlock(false, null, shadowBlock, 
                                                                    null, selectedBlockDirection, currCursorX, currCursorY));
             
            },
            stop: function() {
                 /** 현재 drag하는 Block 생성 버튼 위치 구현 */
                blockContainerThis.setCurrCursorY(currCursorY);

                var selectedBlock = null;
                if (shadowBlock) {
                    selectedBlock = shadowBlock.getSelectBlock();
                    $(shadowBlock.getBlockMainDom()).remove();
                }
           
                /** Board에 생성된 Block에 연결할 경우 */
                if (selectedBlock != null) {
                    newBlock = blockContainerThis.createBlock(blockCodeLineType );
                    selectedBlock.appendBlock(newBlock, selectedBlockDirection);
                    newBlock.renderEditorScrollTop();

                /** Board에 생성된 Block에 연결하지 못한 경우 
                 *  즉 아무대도 연결하지 못하고 생성한 경우
                */
                }  else { 
                    var blockList = blockContainerThis.getBlockList();
                    /** 
                     * Board에 생성된 Block이 1개도 없을 때
                     */
                    if (blockList.length == 0) {
                        newBlock = blockContainerThis.makeNodeBlock();
                        newThisBlock = blockContainerThis.createBlock( blockCodeLineType );

                        blockContainerThis.reNewContainerDom();
                        blockContainerThis.reRenderAllBlock_asc();

                        /** 최초 생성된 root 블럭 set root direction */
                        newBlock.setDirection(BLOCK_DIRECTION.ROOT);
                        newBlock.appendBlock(newThisBlock,BLOCK_DIRECTION.DOWN);

                    /** `
                     * Board에 생성된 Block이 적어도 1개는 있을 때
                     */

                     /** 선택한 블럭이 있을때 */
                    } else if (blockContainerThis.getSelectedBlock() 
                                && blockContainerThis.getSelectedBlock().getBlockCodeLineType() != BLOCK_CODELINE_TYPE.TEXT) {
                        
                        newBlock = blockContainerThis.createBlock(blockCodeLineType );
                        selectedBlock = blockContainerThis.findNodeBlock();
                        selectedBlock.getLastChildBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                        selectedBlock.renderSelectedBlockColor(true);
                        
                    /** 선택한 블럭이 없을때 */
                    }  else {
                        var rootBlock = blockContainerThis.getRootBlock();
                        newBlock = blockContainerThis.makeNodeBlock();
                        newThisBlock = blockContainerThis.createBlock( blockCodeLineType );
                        newBlock.appendBlock(newThisBlock, BLOCK_DIRECTION.DOWN);

                        var currentBlock = blockContainerThis.getRootToLastBottomBlock();
                        /** Class & def or Controls Block들은
                         *  holderBlock을 가지고 있다 */
                        var holderBlock = rootBlock.getHolderBlock();
                        if ( holderBlock != null ) {
                            if (currentBlock == null) {
                                rootBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            } else {
                                currentBlock.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            }
                        } else {
                            if (currentBlock == null) {
                                rootBlock.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            } else {
                                currentBlock.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            }
                        }
    
                        newBlock.renderEditorScrollTop(true);
                    }
                }

                blockContainerThis.stopDragBlock(false, newBlock); 

                shadowBlock = null;
                newBlock = null;
            }
        });
    }

    return CreateBlockBtn;
});
