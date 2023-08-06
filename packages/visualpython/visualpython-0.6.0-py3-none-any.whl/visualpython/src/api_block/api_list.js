define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpXMLHandler'
    , 'nbextensions/visualpython/src/common/component/vpAccordionBox'
    , 'nbextensions/visualpython/src/common/component/vpLineNumberTextArea'
    , 'nbextensions/visualpython/src/common/component/vpIconInputText'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    , './constData.js'
], function ( $, vpCommon, vpConst, sb, xmlHandler, vpAccordionBox, vpLineNumberTextArea,vpIconInputText, vpFuncJS
              , constData ) {

    const { BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION

            , STR_CHANGE_KEYUP_PASTE
            , STR_NULL
            , STR_ONE_SPACE 
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_INPUT_YOUR_CODE
            , STR_COLOR
            , STR_OPTION 
            , STR_BACKGROUND_COLOR 
            , STATE_codeLine
            , COLOR_BLACK
            , COLOR_GRAY_input_your_code

            , VP_ID_PREFIX
            , VP_ID_APIBLOCK_OPTION_CODE_ARG
            , VP_ID_APIBLOCK_LEFT_TAB_API
            
            , VP_CLASS_PREFIX 
            , VP_CLASS_STYLE_DISPLAY_BLOCK
            , VP_CLASS_STYLE_DISPLAY_NONE
            , VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW
            , VP_CLASS_APIBLOCK_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN
            , VP_CLASS_BLOCK_SUB_BTN_CONTAINER
            , VP_CLASS_APIBLOCK_BLOCK_HEADER
            , VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED } = constData;

    const api_listInit = function(blockContainer, blockType) {
        // var uuid = thatBlock.getUUID();
        let xmlLibraries;
        let libraryLoadComplete = false;
        let loadedFuncJS;
        let apiBlockJS;
        let generatedCode;
        let generatedMetaData;
        let loadedFuncID;
        var events;
        let nodeIndex = 0;
        let librarySearchComplete = new Array();
        let searchBoxUUID;
        let isShowNoteNodeDetail = false;
        var mathjaxutils;
        
        let block_closure;
        try {
            // events 에 대한 예외 발생 가능할 것으로 예상.
            // console.log('requirejs',requirejs);
            events = requirejs('base/js/events');
        } catch (err) {
            if (window.events === undefined) {
                var Events = function () { };
                window.events = $([new Events()]);
            }
            events = window.events;
        }
    
        // mathjaxutils 경로 문제 처리 - notebook 패키지 버전 6.1.6부터는 base/js로 이동됨
        try {
            // 6.1.6 version path for mathjaxutils
            mathjaxutils = requirejs('base/js/mathjaxutils');
        } catch (err) {
            console.log('behind 6.1.6... reload mathjaxutils.');
            mathjaxutils = requirejs('notebook/js/mathjaxutils')
        }

        var getOptionPageURL = function(funcID) {
            // console.log('funcID', funcID);
            var sbURL = new sb.StringBuilder();
            
            sbURL.append(Jupyter.notebook.base_url);
            sbURL.append(vpConst.BASE_PATH);
            sbURL.append(vpConst.SOURCE_PATH);

            // 함수 경로 바인딩
            var optionData = $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + funcID + "]");
            var filePath = $(optionData).find(vpConst.LIBRARY_ITEM_FILE_URL_NODE).text();
            // console.log('filePath', filePath);
            // 경로가 조회되지 않는 경우
            if (filePath === undefined || filePath === "") {
                // alert("Function id not founded!");
                filePath = 'markdown/markdown.js';
                // return "";
            }
            // console.log('filePath', filePath);
            sbURL.append(filePath);
            return sbURL.toString();
        }
    
        /**
         * load api block
         */
        var loadApiBlock = function() {
            // library 정보 로드 종료되지 않으면 이벤트로 등록
            if (!libraryLoadComplete) {
                events.on('library_load_complete.vp', loadApiBlock);
                return;
            }

            events.off('library_load_complete.vp', loadApiBlock);
            var loadUrl = getOptionPageURL("api_block");
            // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
            if (loadUrl !== "") {
                // 옵션 로드
                requirejs([loadUrl], function (loaded) {
                    loaded.initOption(apiBlockLoadCallback);
                });
            }
        }

        var addAutoCompleteItem = function(item) {
            // 이미 등록된 항목은 제외한다.
            if (!librarySearchComplete.includes(item)) {
                librarySearchComplete.push(item);
            }
        }

        var setLibraryLoadComplete = function() {
            libraryLoadComplete = true;
            events.trigger('library_load_complete.vp');
        }

        var librariesBind = function(node, container) {
            $(node).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_PACKAGE + "]").each(function() {
                var thisNode = $(this);
                var accboxTopGrp;
                if ($(thisNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) == 0) {
                    accboxTopGrp = makeLibraryTopGroupBox($(thisNode));
                    
                    $(container).append(accboxTopGrp.toTagString());
                }
            });
        }

        var bindSearchAutoComplete = function() {
            $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_FUNCTION + "]").each(function() {
                addAutoCompleteItem($(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
                $(this).attr(vpConst.LIBRARY_ITEM_TAG_ATTR).split(",").forEach(function(tag) {
                    addAutoCompleteItem(tag.trim());
                });
            });
    
            $(vpCommon.wrapSelector(vpCommon.formatString(".{0} input", searchBoxUUID))).autocomplete({
                source: librarySearchComplete
                , classes: {
                    "ui-autocomplete": "vp-search-autocomplete"
                  }
            });
        }

        var libraryLoadCallback = function(container) {
            setLibraryLoadComplete();
            librariesBind($(xmlLibraries.getXML()).children(vpConst.LIBRARY_ITEM_WRAP_NODE), container);
            
            bindSearchAutoComplete();
        };

        var loadLibraries = function(container) {
            var libraryURL = window.location.origin + vpConst.PATH_SEPARATOR + vpConst.BASE_PATH + vpConst.DATA_PATH + vpConst.VP_LIBRARIES_XML_URL;
            xmlLibraries = new xmlHandler.VpXMLHandler(libraryURL);
            xmlLibraries.loadFile(libraryLoadCallback, container);
        }

        /**
         * 최상위 패키지는 아코디언 박스로 생성한다.
         * @param {xmlNode} topGrpNode 최상위 페키지
         */
        var makeLibraryTopGroupBox = function(topGrpNode) {
            var accBox = new vpAccordionBox.vpAccordionBox($(topGrpNode).attr(vpConst.LIBRARY_ITEM_NAME_ATTR), false, true);

            // 추가 클래스 설정
            accBox.addClass(vpConst.ACCORDION_GRAY_BGCOLOR);
            accBox.addClass(vpConst.ACCORDION_SMALL_ARROW);

            // 속성 부여
            accBox.addAttribute(vpConst.LIBRARY_ITEM_DATA_ID, $(topGrpNode).attr(vpConst.LIBRARY_ITEM_ID_ATTR));

            // 자식 그룹 노드 생성
            accBox.appendContent(makeLibraryListsGroupNode(topGrpNode));
            
            return accBox;
        }

        /**
         * 공통 컴퍼넌트 아코디언 박스 내용 표시 토글
         * @param {object} trigger 이벤트 트리거 객체
         */
        var toggleAccordionBoxShow = function(trigger) {
            // 유니크 타입인경우 다른 아코디언 박스를 닫는다.
            if ($(trigger).parent().hasClass("uniqueType")) {
                $(trigger.parent().parent().children(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER)).not($(trigger).parent()).removeClass(vpConst.ACCORDION_OPEN_CLASS));
            }
            $(trigger).parent().toggleClass(vpConst.ACCORDION_OPEN_CLASS);
    
            // API List library 인 경우 추가 처리.
            // if ($(trigger).parent().parent().attr("id") == vpConst.API_LIST_LIBRARY_LIST_CONTAINER) {
            if ($(trigger).parent().parent().attr("id") == VP_ID_APIBLOCK_LEFT_TAB_API) {
                // 하이라이트 처리
                $(trigger).children(vpCommon.formatString(".{0}", vpConst.ACCORDION_HEADER_CAPTION)).addClass(vpConst.COLOR_FONT_ORANGE);

                // $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
                $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API)))
                    .find(vpCommon.formatString(".{0}", vpConst.COLOR_FONT_ORANGE))
                    .not($(trigger).children(vpCommon.formatString(".{0}", vpConst.ACCORDION_HEADER_CAPTION)))
                        .removeClass(vpConst.COLOR_FONT_ORANGE);
                
                closeSubLibraryGroup();
            }
        }

        /**
         * 공통 컴퍼넌트 아코디언 박스 헤더 클릭
         */
        $(document).off("click", vpCommon.wrapSelector(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER), vpCommon.formatString(".{0}", vpConst.ACCORDION_HEADER)));
        $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER), vpCommon.formatString(".{0}", vpConst.ACCORDION_HEADER)), function() {
            toggleAccordionBoxShow($(this));
        });
        /**
         * api option navi info item 클릭
         */
        $(document).off('click', vpCommon.wrapSelector(vpCommon.formatString(".{0}:not(:last-child)", vpConst.OPTION_NAVIGATOR_INFO_NODE)));
        $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString(".{0}:not(:last-child)", vpConst.OPTION_NAVIGATOR_INFO_NODE)), function() {
            goListOnNavInfo($(this));
        });
        /**
         * api list item 클릭
         */
        // $(document).off('click', vpCommon.wrapSelector(vpCommon.formatString(".vp-apiblock-body .{0} li", vpConst.LIST_ITEM_LIBRARY)));
        $(document).off("click",`#vp_apiBlockMainContainer .${vpConst.LIST_ITEM_LIBRARY} li`);
        $(document).on("click",`#vp_apiBlockMainContainer .${vpConst.LIST_ITEM_LIBRARY} li`, function(evt) {
            // console.log('여기 클릭');
            evt.stopPropagation();
            if ($(this).hasClass(vpConst.LIST_ITEM_LIBRARY_GROUP)) {
                toggleApiListSubGroupShow($(this));
            } else if ($(this).hasClass(vpConst.LIST_ITEM_LIBRARY_FUNCTION)) {
                const funcID = $(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, ""));
                const callbackFunc = optionPageLoadCallback;
                const naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + funcID + "]"));
                
                let naviInfo = '';
                let index = 0;
                $(naviInfoTag).each(function() {
                    index++;
                    if ($(this).html()) {
                        naviInfo += $(this).html();
                        naviInfo += ' ';
                        if (index != $(naviInfoTag).length) {
                            naviInfo += '>';
                            naviInfo += ' ';
                        }
                    }
                });

                /** 
                 *  Block color 리셋
                 */ 
                blockContainer.resetBlockList();

                const blockList = blockContainer.getBlockList();
                let thisBlock;
                let newblock_api;
                /** 
                 * Board에 생성된 Block이 1개도 없을 때
                 */
                // console.log('blockList');
                if (blockList.length == 0) {
                    const newBlock_node = blockContainer.makeNodeBlock();
                    newblock_api = blockContainer.createBlock(BLOCK_CODELINE_TYPE.API);
                    newblock_api.setFuncID(funcID);
                    newblock_api.setOptionPageLoadCallback(callbackFunc);
                    newblock_api.setLoadOption(loadOption);
                    newblock_api.setState({
                        [STATE_codeLine]: naviInfo
                    });

                    blockContainer.reNewContainerDom();

                    /** 최초 생성된 root 블럭 set root direction */
                    newBlock_node.setDirection(BLOCK_DIRECTION.ROOT);
                    newBlock_node.appendBlock(newblock_api, BLOCK_DIRECTION.DOWN);
                    blockContainer.reRenderAllBlock_asc();
                    const length = blockContainer.getNodeBlockNumber();
                    $(`#vp_apiblock_nodeblock_${newBlock_node.getUUID()}`).text(`Node ${length}`);

                    thisBlock = newBlock_node;
                } else {
                    newblock_api = blockContainer.createBlock(BLOCK_CODELINE_TYPE.API);
                    newblock_api.setFuncID(funcID);
                    newblock_api.setOptionPageLoadCallback(callbackFunc);
                    newblock_api.setLoadOption(loadOption);
                    newblock_api.setState({
                        [STATE_codeLine]: naviInfo
                    });

                    var nodeBlockList = blockContainer.getNodeBlockList();
                    var selectedBlock = blockContainer.getSelectedBlock();
            
                    if (selectedBlock && selectedBlock.getBlockCodeLineType() != BLOCK_CODELINE_TYPE.TEXT) {
                        nodeBlockList.some(nodeBlock => {
                            var childLowerDepthBlockList = nodeBlock.getChildLowerDepthBlockList();
                            childLowerDepthBlockList.push(nodeBlock);
                            childLowerDepthBlockList.some(block => {
                                if (block.getUUID() == selectedBlock.getUUID()) {
                                    selectedBlock = nodeBlock;
                                }
                            });
                        });
             
                        selectedBlock.getLastChildBlock().appendBlock(newblock_api, BLOCK_DIRECTION.DOWN);
                        selectedBlock.renderSelectedBlockColor(true);
                        thisBlock = newblock_api;
                        blockContainer.reRenderAllBlock_asc();
                    } else {
                     
                        const newBlock_node = blockContainer.makeNodeBlock();
                
                        newBlock_node.appendBlock(newblock_api, BLOCK_DIRECTION.DOWN);

                        const nodeBlockAndTextBlockList = blockContainer.getNodeBlockAndTextBlockList_asc();
                        nodeBlockAndTextBlockList[nodeBlockAndTextBlockList.length -1].getLastChildBlock().appendBlock(newBlock_node, BLOCK_DIRECTION.DOWN);
                        thisBlock = newBlock_node;
                        
                        blockContainer.reRenderAllBlock_asc();
                        const length = blockContainer.getNodeBlockNumber();
                        $(`#vp_apiblock_nodeblock_${newBlock_node.getUUID()}`).text(`Node ${length}`);
                    }
                }
         
                newblock_api.writeCode(naviInfo);
                block_closure = newblock_api;
                blockContainer.reRenderAllBlock_asc();

                loadOption(funcID, callbackFunc);
         
                thisBlock.createSubButton();
                /** block color 색칠 */
                thisBlock.renderMyColor(true);
    
                const blockTab_api = $(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAB_API);
                $(blockTab_api).removeClass(VP_CLASS_STYLE_DISPLAY_BLOCK);
                $(blockTab_api).addClass(VP_CLASS_STYLE_DISPLAY_NONE);
                blockContainer.setIsAPIListPageOpen(false);
                $(".vp-apiblock-blocktab-api").css(STR_BACKGROUND_COLOR, 'white');
            }
        });

        /**
         * api list 그룹 하위 표시 토글
         * @param {object} trigger 이벤트 트리거 객체
         */
        var toggleApiListSubGroupShow = function(trigger) {
            // console.log('$(trigger).parent()',$(trigger).parent());
            // console.log('$(trigger).children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY))',$(trigger).children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)));
            $(trigger).parent().children(vpCommon.formatString("li.{0}", vpConst.LIST_ITEM_LIBRARY_GROUP)).not($(trigger)).find(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).hide();
            $(trigger).children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).toggle();
     
            // 하이라이트 처리
            // $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API)))
                    .find(vpCommon.formatString(".{0}", vpConst.COLOR_FONT_ORANGE))
                    .not($(trigger)).removeClass(vpConst.COLOR_FONT_ORANGE);
            $(trigger).addClass(vpConst.COLOR_FONT_ORANGE);
        }

        /**
         * 옵션 페이지 로드 완료 callback.
         * @param {funcJS} funcJS 옵션 js 객체
         */
        var optionPageLoadCallback = function(funcJS) {
            block_closure.setImportPakage(funcJS);
            const importPakage = block_closure.getImportPakage();
            if (block_closure.getBlockCodeLineType() == BLOCK_CODELINE_TYPE.TEXT) {
                importPakage.setBlock(block_closure);
            }
         
            // console.log('optionPageLoadCallback',optionPageLoadCallback);

            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).empty();
        
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL),
                vpCommon.formatString(".{0}", vpConst.OPTION_NAVIGATOR_INFO_NODE))).remove();
            $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

            // load 옵션 변경시 기존 옵션 이벤트 언바인드 호출.
            if (loadedFuncJS != undefined) {
                loadedFuncJS.unbindOptionEvent();
            }
            loadedFuncJS = funcJS;

            var naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + loadedFuncID + "]"));
            // FIXME: funcJS 내부 id libraries.xml 과 매칭 필요
            // var naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + loadedFuncJS.funcID + "]"));
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL))).append(naviInfoTag);

            // metadata 존재하면 load
            if (loadedFuncJS.metadata !== undefined && loadedFuncJS.metadata != "") {
                loadedFuncJS.loadMeta(loadedFuncJS, generatedMetaData);
            }
            var blockOptionPageDom = makeUpGreenRoomHTML();
            // console.log('blockOptionPageDom makeUpGreenRoomHTML',blockOptionPageDom);
            block_closure.setBlockOptionPageDom(blockOptionPageDom);

            loadedFuncJS.bindOptionEvent();

            block_closure.renderOptionPage();

        }
        /**
         * 그룹 노드 리스트 아이템으로 생성
         * @param {xmlNode} grpNode 그룹 노드
         */
        var makeLibraryListsGroupNode = function(grpNode) {
            var sbGrpNode = new sb.StringBuilder();
            
            sbGrpNode.appendLine(makeLibraryListsFunctionNode(grpNode));
            
            sbGrpNode.appendFormatLine("<ul class='{0}' {1}>", vpConst.LIST_ITEM_LIBRARY, $(grpNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) > 0 ? "style='display:none;'" : "");

            $(grpNode).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_PACKAGE + "]").each(function() {
                sbGrpNode.appendFormatLine("<li class='{0}' {1}='{2}'>{3}"
                    , vpConst.LIST_ITEM_LIBRARY_GROUP, vpConst.LIBRARY_ITEM_DATA_ID, $(this).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
                
                sbGrpNode.appendLine(makeLibraryListsGroupNode($(this)));
                
                sbGrpNode.appendLine("</li>");
            });
            sbGrpNode.appendLine("</ul>");
            
            return sbGrpNode.toString();
        }
        /**
         * 함수 노드 리스트 아이템으로 생성
         * @param {xmlNode} grpNode 그룹 노드
         */
        var makeLibraryListsFunctionNode = function(grpNode) {
            var sbFuncNode = new sb.StringBuilder();

            sbFuncNode.appendFormatLine("<ul class='{0}' {1}>", vpConst.LIST_ITEM_LIBRARY, $(grpNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) > 0 ? "style='display:none;'" : "");

            $(grpNode).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_FUNCTION + "]").each(function() {
                sbFuncNode.appendFormatLine("<li class='{0}' {1}='{2}'>{3}</li>"
                    , vpConst.LIST_ITEM_LIBRARY_FUNCTION, vpConst.LIBRARY_ITEM_DATA_ID, $(this).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
            });

            sbFuncNode.appendLine("</ul>");

            return sbFuncNode.toString();
        }
        /**
         * api list library 검색
         * @param {String} keyword 검색어
         */
        var searchAPIList = function(keyword) {
            alert(vpCommon.formatString("search keyword > {0}", keyword));
        }

        /**
         * api list 그룹 하위 모두 숨기기
         */
        var closeSubLibraryGroup = function() {
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER), 
                vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTENT_CLASS))).children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY))
                    .find(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).hide();
        }

        /**
         * 옵션 페이지 로드
         * @param {String} funcID xml 함수 id
         * @param {function} callback 로드 완료시 실행할 함수
         * @param {JSON} metadata 메타데이터
         */
        var loadOption = function(funcID, callback, metadata) {
            var loadUrl = getOptionPageURL(funcID);
            // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
            if (loadUrl !== "") {
                // 옵션 로드
                loadedFuncID = funcID;
                generatedCode = undefined;
                generatedMetaData = metadata;
                requirejs([loadUrl], function (loaded) {
                    // console.log('loaded',loaded);
                    loaded.initOption(callback, metadata);
                });
            }
        }
        var loadOption_textBlock = function(funcID, callback, metadata) {
            var loadUrl = '/nbextensions/visualpython/src/markdown/markdown.js';
            // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
            if (loadUrl !== "") {
                // 옵션 로드
                loadedFuncID = funcID;
                generatedCode = undefined;
                generatedMetaData = metadata;
                requirejs([loadUrl], function (loaded) {
                    // console.log('loaded',loaded);
                    loaded.initOption(callback, metadata);
                });
            }
        }
        /**
         * 로드된 함수 경로 바인딩
         * @param {xmlNode} node node for binding
         */
        var makeOptionPageNaviInfo = function(node) {
            var sbNaviInfo = new sb.StringBuilder();
            
            if ($(node).parent().attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) !== undefined) {
                sbNaviInfo.appendLine(makeOptionPageNaviInfo($(node).parent()));
            }

            sbNaviInfo.appendFormatLine("<span class='{0}' {1}={2}>{3}</span>"
                , vpConst.OPTION_NAVIGATOR_INFO_NODE, vpConst.LIBRARY_ITEM_DATA_ID, $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
                
            return sbNaviInfo.toString();
        }

            /**
         * 로딩된 옵션 페이지 html 처리
         */
        var makeUpGreenRoomHTML = function() {
            // console.log('makeUpGreenRoomHTML',makeUpGreenRoomHTML);
            var that;
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM), vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE))).each(function() {
                $(this).find("h4:eq(0)").hide();
                $(this).find("hr:eq(0)").hide();
                $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).append($(this));
                $(vpCommon.wrapSelector(vpCommon.formatString(".{0}", VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW))).append($(this));

                // console.log('$(this)',$(this));

                // blockContainer

                // $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API))).append($(this));
                that = $(this);
            });

            openOptionBook();

            return that;
        }

            /**
         * open api option container
         */
        var openOptionBook = function() {
            // $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER))).hide();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API))).hide();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_CONTAINER))).show();
        }

        /**
         * 로드된 옵션 페이지 닫기
         */
        var closeOptionBook = function() {
            // $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER))).show();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API))).show();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_CONTAINER))).hide();
            
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL),
                vpCommon.formatString(".{0}", vpConst.OPTION_NAVIGATOR_INFO_NODE))).remove();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).children().remove();

            // $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API))).children().remove();
            $(vpCommon.wrapSelector(vpCommon.formatString(".{0}", VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW))).children().remove();
            
        }
        /**
         * 네비 항목 클릭하여 리스트로 이동
         * @param {object} trigger 이벤트 트리거 객체
         */
        var goListOnNavInfo = function(trigger) {

            // var obj = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
            var obj = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API)))
                .children(vpCommon.formatString("div[{0}={1}]", vpConst.LIBRARY_ITEM_DATA_ID, $(trigger).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, ""))));

            // 최상위 그룹클릭인 경우
            if (obj.length > 0) {
                // 유니크 타입인경우 다른 아코디언 박스를 닫는다.
                if ($(obj).hasClass("uniqueType")) {
                    $(obj.parent().children(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER)).not($(obj)).removeClass(vpConst.ACCORDION_OPEN_CLASS));
                }
                $(obj).addClass(vpConst.ACCORDION_OPEN_CLASS);
                // 하위 그룹 닫기
                closeSubLibraryGroup();
                closeOptionBook();
            } else {
                closeSubLibraryGroup();
                // obj = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
                obj = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API)))
                    .find(vpCommon.formatString("[{0}={1}]", vpConst.LIBRARY_ITEM_DATA_ID, $(trigger).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, ""))));
                
                obj.children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).show();
                var objParent = obj.parent();
                for (var loopSafety = 0; loopSafety < 10; loopSafety++) {
                    // 부모 리스트 존재하면 표시
                    if ($(objParent).hasClass(vpConst.LIST_ITEM_LIBRARY)) {
                        $(objParent).show();
                    } else if ($(objParent).hasClass(vpConst.ACCORDION_CONTAINER)) {
                        // 유니크 타입인경우 다른 아코디언 박스를 닫는다.
                        if ($(objParent).hasClass("uniqueType")) {
                            $(objParent.parent().children(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER)).not($(objParent)).removeClass(vpConst.ACCORDION_OPEN_CLASS));
                        }
                        $(objParent).addClass(vpConst.ACCORDION_OPEN_CLASS);
                    }
                    objParent = $(objParent).parent();
                    
                    // 부모가 api list contianer 이면 종료
                    // if ($(objParent).attr("id") == vpConst.API_LIST_LIBRARY_LIST_CONTAINER) {
                    //     break;
                    // }
                    if ($(objParent).attr("id") == VP_ID_APIBLOCK_LEFT_TAB_API) {
                        break;
                    }
                }
                closeOptionBook();
            }
        }

        if ( blockType == BLOCK_CODELINE_TYPE.TEXT) {
            loadLibraries(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAB_API);
   
            const textBlockFuncID = 'com_markdown';
            /** 
             * Board에 생성된 Block이 1개도 없을 때
             */
            // console.log('blockList');
            var newBlock_text;
            const blockList = blockContainer.getBlockList();
            if (blockList.length == 0) {
                newBlock_text = blockContainer.makeTextBlock();
                newBlock_text.setDirection(BLOCK_DIRECTION.ROOT);
                newBlock_text.setFuncID(textBlockFuncID);
                newBlock_text.setOptionPageLoadCallback(optionPageLoadCallback);
                newBlock_text.setLoadOption(loadOption);
                block_closure = newBlock_text;

                blockContainer.reNewContainerDom();
                blockContainer.reRenderAllBlock_asc();     
            } else {
                newBlock_text = blockContainer.makeTextBlock();
                newBlock_text.setDirection(BLOCK_DIRECTION.ROOT);
                newBlock_text.setFuncID(textBlockFuncID);
                newBlock_text.setOptionPageLoadCallback(optionPageLoadCallback);
                newBlock_text.setLoadOption(loadOption);
                block_closure = newBlock_text;
                
                const rootBlock = blockContainer.getRootBlock();
                const childBlockList = rootBlock.getChildBlockList();
                childBlockList[childBlockList.length - 1].appendBlock(newBlock_text, BLOCK_DIRECTION.DOWN);
                blockContainer.reRenderAllBlock_asc();
            }
   
            loadOption_textBlock(textBlockFuncID, optionPageLoadCallback);
            return;
        }

        $(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAB_API).empty();

        var searchBox = new vpIconInputText.vpIconInputText();
        searchBox.setIconClass("srch-icon");
        searchBox.setPlaceholder("search");
        searchBoxUUID = searchBox._UUID;
        
        // 검색 아이콘 클릭 이벤트 바인딩
        searchBox.addEvent("click", "icon", function() { searchAPIList($(this).parent().children("input").val()); });
        searchBox.addEvent("keydown", "text", function(evt) {
            if (evt.keyCode == 13) {
                evt.preventDefault();
                searchAPIList($(this).parent().children("input").val());
            }
        });

        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", VP_ID_APIBLOCK_LEFT_TAB_API))).append(searchBox.toTagString());
        loadLibraries(VP_ID_PREFIX + VP_ID_APIBLOCK_LEFT_TAB_API);

    }

    return { api_listInit };
});
