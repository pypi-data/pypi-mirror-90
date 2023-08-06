define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'

    , './api.js'    

    , './constData.js'
    , './blockContainer.js'
    , './createBlockBtn.js'
    , './blockRenderer.js'
    , './api_list.js'

    , './component/boardMenuBar.js'
], function ( $, vpCommon, vpConst, 
              api, constData, blockContainer, createBlockBtn, blockRenderer, api_list,
              apiBlockMenuInit ) {
 
    const { ControlToggleInput
            , LoadVariableList } = api;
  
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , FOCUSED_PAGE_TYPE
            , BLOCK_DIRECTION

            , VP_ID_PREFIX
            , VP_ID_WRAPPER
            , VP_ID_APIBLOCK_LEFT_TAB_API
            , VP_ID_APIBLOCK_LEFT_TAP_APILIST_PAGE
            
            , VP_CLASS_PREFIX
            , VP_CLASS_APIBLOCK_MAIN
            , VP_CLASS_APIBLOCK_BODY
            , VP_CLASS_APIBLOCK_BOARD_CONTAINER
            , VP_CLASS_APIBLOCK_MENU_BTN
            , VP_CLASS_MAIN_CONTAINER
            , VP_CLASS_APIBLOCK_TITLE
            , VP_CLASS_APIBLOCK_CODELINE_ELLIPSIS
            , VP_CLASS_STYLE_DISPLAY_FLEX

            , API_BLOCK_PROCESS_PRODUCTION
            , API_BLOCK_PROCESS_DEVELOPMENT
            , VP_CLASS_APIBLOCK_BUTTONS
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_OPTION_TAB


            , VP_CLASS_STYLE_DISPLAY_BLOCK
            , VP_CLASS_STYLE_DISPLAY_NONE

            , NUM_DELETE_KEY_EVENT_NUMBER
            , NUM_APIBLOCK_MAIN_PAGE_WIDTH
            , NUM_APIBLOCK_LEFT_PAGE_WIDTH
            , NUM_OPTION_PAGE_WIDTH
            , NUM_API_BOARD_CENTER_PAGE_WIDTH

            , STR_TOP
            , STR_SCROLL
            , STR_CLICK
      
            , STR_WIDTH 
    
            , STR_DISPLAY
       
            , STR_BLOCK
            , STR_PARENT
            , STR_NONE
            , STR_NOTEBOOK
            , STR_HEADER
            , STR_CELL
            , STR_CODEMIRROR_LINES

            , STATE_codeLine } = constData;

    const BlockContainer = blockContainer;
    const CreateBlockBtn = createBlockBtn;
    const { api_listInit } = api_list;

    var init = function(){
        $.fn.single_double_click = function(single_click_callback, double_click_callback, timeout) {
            return this.each(function(){
                var clicks = 0, 
                    self = this;
                $(this).click(function(event){
                    clicks++;
                    if (clicks == 1) {
                        setTimeout(function(){
                            if(clicks == 1) {
                                single_click_callback.call(self, event);
                            } else {
                                double_click_callback.call(self, event);
                            }
                            clicks = 0;
                        }, timeout || 300);
                    }
                });
            });
        }

        /** block container 생성
         * 싱글톤 무조건 1개
         */
        var blockContainer = new BlockContainer();
        var createBlockBtnArray = Object.values(BLOCK_CODELINE_BTN_TYPE);
        createBlockBtnArray.forEach(enumData => {
            new CreateBlockBtn(blockContainer, enumData);
        });

        /**  블럭 up down 버튼 bind Event함수 */
        apiBlockMenuInit(blockContainer);
        var optionPageRectWidth = blockContainer.getOptionPageWidth();
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_DISPLAY, STR_BLOCK);
                       
        var mainPageRect = $(VP_ID_PREFIX + VP_ID_WRAPPER)[0].getBoundingClientRect();
        var mainPageRectWidth = mainPageRect.width; 
        if (mainPageRectWidth == 0) {
            mainPageRectWidth = NUM_APIBLOCK_MAIN_PAGE_WIDTH;
        }
        var buttonsPageRectWidth = NUM_APIBLOCK_LEFT_PAGE_WIDTH; 
        var boardPageRectWidth = NUM_API_BOARD_CENTER_PAGE_WIDTH;
        var optionPageRectWidth = mainPageRectWidth - buttonsPageRectWidth - boardPageRectWidth - 45;
        // var optionPageRectWidth = NUM_OPTION_PAGE_WIDTH;
        // var boardPageRectWidth = mainPageRectWidth - buttonsPageRectWidth - optionPageRectWidth - 55;
        // console.log('mainPageRectWidth', mainPageRectWidth);
        // console.log('buttonsPageRectWidth', buttonsPageRectWidth);
        // console.log('optionPageRectWidth', optionPageRectWidth);
        // console.log('boardPageRectWidth', boardPageRectWidth);

        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).css(STR_WIDTH, optionPageRectWidth);
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).css(STR_WIDTH, boardPageRectWidth);

        $("#vp_apiblock_board_main_title input").val('Untitled');
        $("#vp_apiblock_board_main_title input").focus();

        /** block을 클릭하고 delete 키 눌렀을 때 */ 
        $(document).keyup(function(e) {
            var keycode =  e.keyCode 
                                ? e.keyCode 
                                : e.which;

            if (keycode == NUM_DELETE_KEY_EVENT_NUMBER
                && blockContainer.getFocusedPageType() == FOCUSED_PAGE_TYPE.EDITOR){
                var selectedBlock = blockContainer.getSelectedBlock();
                selectedBlock.clickBlockDeleteButton();
            } 

            
            if ($("#vp_apiblock_board_makenode_input").is(":focus") 
                && window.event.keyCode == 13) {
                var inputNodeBlockTitleName = $("#vp_apiblock_board_makenode_input").val();
                if (inputNodeBlockTitleName == '') {
                    vpCommon.renderAlertModal('Required input!');
                    $("#vp_apiblock_board_makenode_input").val('');
                    return;
                }

                if (blockContainer.getBlockList().length == 0) {
                    var newBlock = blockContainer.createBlock(BLOCK_CODELINE_TYPE.NODE);
                    newBlock.setState({
                        [STATE_codeLine]: inputNodeBlockTitleName
                    });

                    blockContainer.deleteContainerDom();
                    var containerDom = blockContainer.makeContainerDom();

                    $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(containerDom);
        
                    /** 최초 생성된 root 블럭 set root direction */
                    newBlock.setDirection(BLOCK_DIRECTION.ROOT);

                    blockContainer.reRenderAllBlock_asc();

                } else {
                    var newBlock = blockContainer.createBlock(BLOCK_CODELINE_TYPE.NODE);
                    newBlock.setState({
                        [STATE_codeLine]: inputNodeBlockTitleName
                    });

                    var rootBlock = blockContainer.getRootBlock();
                    var childBlockList = rootBlock.getChildBlockList();
                    childBlockList[childBlockList.length-1].appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
    
                    blockContainer.reRenderAllBlock_asc();
                    newBlock.renderEditorScrollTop();
                }

                newBlock.writeCode(inputNodeBlockTitleName);
                /** 입력 input 초기화 */
                $("#vp_apiblock_board_makenode_input").val('');
            }

            if(window.event.keyCode == 13) {
                // console.log('노드 블럭?');
                var selectedBlock = blockContainer.getSelectedBlock();
                if (selectedBlock 
                    && selectedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.NODE) {
                        var blockUUID = selectedBlock.getUUID();
                        selectedBlock.setIsNodeBlockInput(false);
                        $(`.vp-apiblock-nodeblock-input-${blockUUID}`).css(STR_DISPLAY, STR_NONE);
                        $(`.vp-apiblock-nodeblock-${blockUUID}`).css(STR_DISPLAY, STR_BLOCK);
                        selectedBlock.renderOptionPage();
                }
            }
        });

        $(document).on("click",`.vp-apiblock-panel-area-vertical-btn`, function(){
             if ($(this).hasClass(`vp-apiblock-arrow-down`)) {
                $(`.vp-apiblock-panel-area-vertical-btn`).removeClass(`vp-apiblock-arrow-up`);
                $(`.vp-apiblock-panel-area-vertical-btn`).addClass(`vp-apiblock-arrow-down`);
                $(`.vp-apiblock-panel-area-vertical-btn`).parent().parent().addClass(`vp-apiblock-minimize`);

                $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API)))
                    .find(vpCommon.formatString(".{0}", vpConst.COLOR_FONT_ORANGE)).removeClass(vpConst.COLOR_FONT_ORANGE);
              
                $(`#vp_apiblock_left_tab_api .uniqueType`).removeClass(vpConst.ACCORDION_OPEN_CLASS);
                $(".vp-block-blocktab-name").removeClass(vpConst.COLOR_FONT_ORANGE);
                
                $(this).next().addClass(vpConst.COLOR_FONT_ORANGE);
                $(this).removeClass(`vp-apiblock-arrow-down`);
                $(this).addClass(`vp-apiblock-arrow-up`);
                $(this).parent().parent().removeClass(`vp-apiblock-minimize`);
             } else {
                $(this).next().removeClass(vpConst.COLOR_FONT_ORANGE);
                $(this).removeClass(`vp-apiblock-arrow-up`);
                $(this).addClass(`vp-apiblock-arrow-down`);
                $(this).parent().parent().addClass(`vp-apiblock-minimize`);
             }
        });
         
        $(document).on("click",`.vp-block-blocktab-name`, function(){
            var $arrowBtn = $(this).prev();
            if ($($arrowBtn).hasClass(`vp-apiblock-arrow-down`)) {
                $(`.vp-apiblock-panel-area-vertical-btn`).removeClass(`vp-apiblock-arrow-up`);
                $(`.vp-apiblock-panel-area-vertical-btn`).addClass(`vp-apiblock-arrow-down`);
                $(`.vp-apiblock-panel-area-vertical-btn`).parent().parent().addClass(`vp-apiblock-minimize`);

                $(".vp-block-blocktab-name").removeClass(vpConst.COLOR_FONT_ORANGE);
                $(this).addClass(vpConst.COLOR_FONT_ORANGE);

                $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API)))
                    .find(vpCommon.formatString(".{0}", vpConst.COLOR_FONT_ORANGE)).removeClass(vpConst.COLOR_FONT_ORANGE);

                $(`#vp_apiblock_left_tab_api .uniqueType`).removeClass(vpConst.ACCORDION_OPEN_CLASS);

                $($arrowBtn).removeClass(`vp-apiblock-arrow-down`);
                $($arrowBtn).addClass(`vp-apiblock-arrow-up`);
                $($arrowBtn).parent().parent().removeClass(`vp-apiblock-minimize`);
            } else {

                $(this).removeClass(vpConst.COLOR_FONT_ORANGE);

                $($arrowBtn).removeClass(`vp-apiblock-arrow-up`);
                $($arrowBtn).addClass(`vp-apiblock-arrow-down`);
                $($arrowBtn).parent().parent().addClass(`vp-apiblock-minimize`);
            }
        });

        $(document).on("click",`#vp_apiblock_left_tab_api .uniqueType`, function(){
            $(".vp-block-blocktab-name").removeClass(vpConst.COLOR_FONT_ORANGE);
            $(`.vp-apiblock-panel-area-vertical-btn`).removeClass(`vp-apiblock-arrow-up`);
            $(`.vp-apiblock-panel-area-vertical-btn`).addClass(`vp-apiblock-arrow-down`);
            $(`.vp-apiblock-panel-area-vertical-btn`).parent().parent().addClass(`vp-apiblock-minimize`);
        });

        $('#vp_block_blocktab_name_title').click(function(event) {
            const blockTab_api = $(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAB_API);
            if(blockContainer.getIsAPIListPageOpen() == true){
                $(blockTab_api).removeClass(VP_CLASS_STYLE_DISPLAY_BLOCK);
                $(blockTab_api).addClass(VP_CLASS_STYLE_DISPLAY_NONE);
                blockContainer.setIsAPIListPageOpen(false);
                $('.vp-apiblock-blocktab-api').css('background-color', 'white');
            } else {
                api_listInit(blockContainer);
                $(blockTab_api).removeClass(VP_CLASS_STYLE_DISPLAY_NONE);
                $(blockTab_api).addClass(VP_CLASS_STYLE_DISPLAY_BLOCK);
                blockContainer.setIsAPIListPageOpen(true);
                $('.vp-apiblock-blocktab-api').css('background-color', '#F5F5F5');
                blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.API_LIST_TAB);
            }
        });

        /** 0.6 버전에서 disabled */
        /** API Block 화면 좌우로 resize 이벤트 함수 */
        // $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).resizable({
        //     containment: STR_PARENT,
        //     handles: 'w',
        //     resizeHeight: false
        //     ,resize:(function() {
        //         blockContainer.setOptionPageResize(true);
        //         blockContainer.resizeOptionPopup();
        //     })
        //     ,stop: function(event, ui) { 
        //         blockContainer.setOptionPageResize(false);
        //     }
        // });

        /** api block 화면 이외에 화면을 클릭했을 때, page 포커스 해제 */
        $(vpCommon.wrapSelector(`${VP_ID_PREFIX}${STR_NOTEBOOK}, 
           ${VP_ID_PREFIX}${STR_HEADER}, 
           ${VP_CLASS_PREFIX}${STR_CELL}, 
           ${VP_CLASS_PREFIX}${STR_CODEMIRROR_LINES}`)).click(function(e) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.NULL);
        });
        
        /** Create block buttons page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BUTTONS)).click(function(event) {
            if ($(event.target).attr('id') == undefined) {
                blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BUTTONS);
                $('.vp-apiblock-blocktab-api').css('background-color', 'white');
            } 

        });

        /** Block Board page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).click(function(event) {
            if ($(event.target).attr('class')
                && ($(event.target).attr('class').indexOf('vp-apiblock-board-body') != -1 
                    || $(event.target).attr('class').indexOf('vp-block-container') != -1 ) ) {
                blockContainer.resetBlockList();
                blockContainer.setSelectedBlock(null);
                blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
            }
            $('.vp-apiblock-blocktab-api').css('background-color', 'white');
        });

        /** Block Board 위 Input 영역을 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_ID_PREFIX + "vp_apiblock_board_main_title")).click(function(event) {
            blockContainer.resetBlockList();
            blockContainer.setSelectedBlock(null);
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.BOARD_TITLE);
            $('.vp-apiblock-blocktab-api').css('background-color', 'white');
        });

        /** API List를 클릭했을 때*/
        $(vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAP_APILIST_PAGE)).click(function(event) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.API_LIST_TAB);
            $('.vp-apiblock-blocktab-api').css('background-color', 'white');
        });

        /** Option page를 클릭했을 때 */
        $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_OPTION_TAB)).click(function(event) {
            blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.OPTION);
            $('.vp-apiblock-blocktab-api').css('background-color', 'white');
        });

        var containerDom = blockContainer.makeContainerDom();
        $(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD).append(containerDom);
        
        $(document).ready(function() {
            var ctrlDown = false,
                ctrlKey = 17,
                cmdKey = 91,
                vKey = 86,
                cKey = 67;
        
            $(document).keydown(function(e) {
                if (e.keyCode == ctrlKey || e.keyCode == cmdKey) {
                    ctrlDown = true;
                }
            }).keyup(function(e) {
                if (e.keyCode == ctrlKey || e.keyCode == cmdKey) {
                    ctrlDown = false;
                }
            });

            $(document).keydown(function(e) {
                /** ctrl + c */
                if (ctrlDown && (e.keyCode == cKey)) {
                    var selectedBlock = blockContainer.getSelectedBlock();
                    if (selectedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
                        return;
                    }   
                    blockContainer.setCtrlSaveData();
                }
                /** ctrl + v */
                if (ctrlDown && (e.keyCode == vKey)) {
                    var selectedBlock = blockContainer.getSelectedBlock();
                    if (selectedBlock.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
                        return;
                    }   

                    const { lastBlock, lastCopyBlocklist_cloned } = blockContainer.getCtrlSaveData();

                    blockContainer.deleteContainerDom();
                    blockContainer.makeContainerDom();

                    lastBlock.appendBlock(lastCopyBlocklist_cloned, BLOCK_DIRECTION.DOWN);
                    
                    blockContainer.calculateDepthFromRootBlockAndSetDepth();
                    blockContainer.reRenderBlockList(true);
                    blockContainer.renderBlockLineNumberInfoDom(true);

                    blockContainer.setCtrlSaveData();

                    var blockList = lastCopyBlocklist_cloned.getChildLowerDepthBlockList();
                    blockList.forEach(block => {
                        block.renderSelectedBlockColor(true);
                    });
                    lastCopyBlocklist_cloned.renderSelectedMainBlockBorderColor(false);

                    vpCommon.renderSuccessMessage('Blocks copy success!');
                }
            });
        });

        $(document).click(function(e) { 
            const targetDom = $(e.target).parent().parent().parent();
   
            if (targetDom.attr('class')) {
                if(targetDom.attr('class').indexOf("vp-apiblock-left-tab-api") != -1
                    || targetDom.attr('class').indexOf("vp-apiblock-left") != -1
                    || targetDom.attr('class').indexOf("vp-apiblock-tab-navigation-body") != -1
                    || targetDom.attr('class').indexOf("vp-apiblock-tab-navigation-node-block") != -1
                    || targetDom.attr('class').indexOf("vp-apiblock-tab-navigation-node-container") != -1
                    || targetDom.attr('class').indexOf("vp-tab-page") != -1) { 
                    
                } else {
                    // console.log('영역 밖입니다.');
                    const blockTab_api = $(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAB_API);
                    $(blockTab_api).removeClass(VP_CLASS_STYLE_DISPLAY_BLOCK);
                    $(blockTab_api).addClass(VP_CLASS_STYLE_DISPLAY_NONE);
                    blockContainer.setIsAPIListPageOpen(false);
                }
            }
            e.stopPropagation();
        });



        /** FIXME: 임시 */
        $(document).on(STR_CLICK, vpCommon.formatString(".{0}", 'vp-tab-header li:nth-child(2)'), function(event) {
            LoadVariableList(blockContainer);
            blockContainer.renderBlockOptionTab();
        });

        ControlToggleInput();
        return blockContainer;
    }

    return init;
});
