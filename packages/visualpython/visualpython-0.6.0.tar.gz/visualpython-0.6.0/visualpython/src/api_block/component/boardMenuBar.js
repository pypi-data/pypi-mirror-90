define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../api.js'    

    , '../constData.js'
    , '../createBlockBtn.js'
    
], function ( $, vpCommon, vpConst, sb, api,constData, createBlockBtn) {
    const { ControlToggleInput
            , JQueryPutCursorAtEnd } = api;

    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , FOCUSED_PAGE_TYPE

            , VP_ID_PREFIX
            , VP_ID_APIBLOCK_VIEWDEPTH
            , VP_ID_APIBLOCK_LINENUMBER_ASC
            , VP_ID_APIBLOCK_DELETE_BLOCK_ALL
            , VP_ID_APIBLOCK_CLOSE

            , VP_CLASS_PREFIX
            , VP_CLASS_APIBLOCK_BOARD
            , VP_CLASS_APIBLOCK_MENU_BTN
            , VP_CLASS_APIBLOCK_OPTION_TAB
            , VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN
            , VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW
            , VP_CLASS_APIBLOCK_OPTION_TAB_CHILDS_OPTION
            , VP_CLASS_APIBLOCK_BOTTOM_OPTIONAL_TAB_VIEW

            , STR_OPTION 
            , STR_CLICK
            , STR_OPACITY } = constData;

    var apiBlockMenuInit = function(blockContainer) {
        var apiBlockMenuBarDom;

        /** board 메뉴 박스 생성 클릭 이벤트 함수 */
        $(document).off(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString(".{0}", VP_CLASS_APIBLOCK_MENU_BTN)));
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString(".{0}", VP_CLASS_APIBLOCK_MENU_BTN)), function(event) {
         
            var isMenubarOpen = blockContainer.getIsMenubarOpen();
            if (isMenubarOpen == true) {
                blockContainer.setIsMenubarOpen(false);   
                    /** board 메뉴 박스 삭제 */
                $(apiBlockMenuBarDom).remove(); 
            
            } else {
                var isShowDepth = blockContainer.getIsShowDepth();
                var isShowDepthStr = '';
                if (isShowDepth == true) {
                    isShowDepthStr = 'off';
                } else {
                    isShowDepthStr = 'on';
                }
                blockContainer.setIsMenubarOpen(true);
                    /** board 메뉴 박스 생성 */
                renderThisComponent(isShowDepthStr);
            }
            event.stopPropagation();
        });
 

        /** Block Depth 보이기 안보이기 on/off 이벤트 함수 */
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_VIEWDEPTH)), function(event) {
            
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 

            var blockList = blockContainer.getBlockList();
            var isShowDepth = blockContainer.getIsShowDepth();
            /** Block depth 보이기 on*/
            if (isShowDepth == true) {
                blockList.forEach(block => {
                    $(block.getBlockDepthInfoDom()).css(STR_OPACITY, 0);
                });
                $(vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_VIEWDEPTH)).text(`View depth on`);
                blockContainer.setIsShowDepth(false);
            /** Block depth 안 보이기 off */             
            } else {
                blockList.forEach(block => {
                    if (block.getDepth() == 0) {
                        return;
                    }
                    $(block.getBlockDepthInfoDom()).css(STR_OPACITY, 1);
                });
                $(vpCommon.wrapSelector(VP_ID_PREFIX + VP_ID_APIBLOCK_VIEWDEPTH)).text(`View depth off`);
                blockContainer.setIsShowDepth(true);
            }
    
            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });
  
        /** Board위에 존재하는 모든 Block 삭제 이벤트 함수 */
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_DELETE_BLOCK_ALL)), function(event) {
       
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 
      
            var rootBlock = blockContainer.getRootBlock();
            if (rootBlock) {
                rootBlock.deleteBlock();
                rootBlock.resetOptionPage();
            
                // blockContainer.setBlockList([]);
                blockContainer.setFocusedPageTypeAndRender(FOCUSED_PAGE_TYPE.EDITOR);
                $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_BOARD)).animate({
                    scrollTop: 0 
                }, 100);

                blockContainer.reNewContainerDom();
                blockContainer.reRenderAllBlock_asc();
            }
            
            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });

        /** board 메뉴 창을 클릭하면 메뉴를 닫음
         */
        $(document).on(STR_CLICK, vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.VP_NOTE_EXTRA_MENU_CONTAINER)), function(event) {
            /** board 메뉴 박스 삭제 */
            $(apiBlockMenuBarDom).remove(); 

            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });

    
        $(document).on(STR_CLICK, function(event) {
            $(apiBlockMenuBarDom).remove(); 

            blockContainer.setIsMenubarOpen(false);
            event.stopPropagation();
        });

        /** board 메뉴 박스 렌더링 */
        var renderThisComponent = function(isShowDepthStr) {
            // vpConst.VP_NOTE_EXTRA_MENU_BTN
            var sbAPIBlockMenu = new sb.StringBuilder();
            sbAPIBlockMenu.appendFormatLine("<div id='{0}'  style='{1}'>", vpConst.VP_NOTE_EXTRA_MENU_BTN, 'display: block;');
            sbAPIBlockMenu.appendFormatLine("<div id='{0}' >", vpConst.VP_NOTE_EXTRA_MENU_CONTAINER, );
            sbAPIBlockMenu.appendFormatLine("<ul class='{0}'>", vpConst.VP_NOTE_EXTRA_MENU_LIST);

            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>{2}</li>"
                , vpConst.VP_EXCEPT_BIND, vpConst.VP_NOTE_EXTRA_MENU_NEW_NOTE, vpConst.VP_NOTE_EXTRA_MENU_NEW_NOTE_CAPTION);
            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>{2}</li>"
                , vpConst.VP_EXCEPT_BIND, vpConst.VP_NOTE_EXTRA_MENU_OPEN_NOTE, vpConst.VP_NOTE_EXTRA_MENU_OPEN_NOTE_CAPTION);

            sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>{2}</li>"
                , vpConst.VP_EXCEPT_BIND, vpConst.VP_NOTE_EXTRA_MENU_SAVE_NOTE, vpConst.VP_NOTE_EXTRA_MENU_SAVE_NOTE_CAPTION);
            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>{2}</li>"
                , vpConst.VP_EXCEPT_BIND, vpConst.VP_NOTE_EXTRA_MENU_SAVE_AS_NOTE, vpConst.VP_NOTE_EXTRA_MENU_SAVE_AS_NOTE_CAPTION);

            sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, VP_ID_APIBLOCK_VIEWDEPTH);
            sbAPIBlockMenu.appendFormatLine("{0}</li>", 'View depth ' + isShowDepthStr);

            sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

      

            sbAPIBlockMenu.appendFormatLine("<li class='{0}' id='{1}'>", vpConst.VP_EXCEPT_BIND, VP_ID_APIBLOCK_DELETE_BLOCK_ALL);
            sbAPIBlockMenu.appendFormatLine("{0}</li>", 'Delete all block');

            // sbAPIBlockMenu.appendFormatLine("<hr class='{0}'/>", vpConst.VP_NOTE_EXTRA_MENU_LINE);

            sbAPIBlockMenu.appendLine("</ul>");
            sbAPIBlockMenu.appendLine("</div>");
            sbAPIBlockMenu.appendLine("</div>");
            /** board 메뉴 박스 생성 */
            apiBlockMenuBarDom = $(sbAPIBlockMenu.toString());

            /** board 메뉴 버튼아래에 메뉴 박스 생성 */
            $(vpCommon.wrapSelector(VP_CLASS_PREFIX + VP_CLASS_APIBLOCK_MENU_BTN)).append(apiBlockMenuBarDom);
        }
    }

    return apiBlockMenuInit;

});