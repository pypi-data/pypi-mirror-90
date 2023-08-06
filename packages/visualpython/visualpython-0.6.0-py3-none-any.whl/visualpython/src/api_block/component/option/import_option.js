define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'

    , '../../api.js'    
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, 

              api
              , constData
              , blockRenderer
              , baseComponent ) {

    const { ChangeOldToNewState
        , FindStateValue

        , CreateOneArrayValueAndGet
        , UpdateOneArrayValueAndGet
        , DeleteOneArrayValueAndGet

        , DestructureFromBlockArray

        , MakeFirstCharToUpperCase
        , MapTypeToName
        , RemoveSomeBlockAndGetBlockList
        , ShuffleArray
        , GetImageUrl
        , ControlToggleInput } = api;

    const { RenderDefaultOrDetailButton
            , RenderInputRequiredColor

            , RenderDefaultImportDom
            , RenderCustomImportDom
            , RenderDefaultOrCustomImportContainer
            , ShowImportListAtBlock } = blockRenderer;

    const { BLOCK_DIRECTION
            , BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , IMPORT_BLOCK_TYPE

            , STR_COLON_SELECTED
            , STR_NULL
            , STR_FOR
            , STR_INPUT
            , STR_CLICK
            , STR_CHANGE
            , STR_CHANGE_KEYUP_PASTE

            , STR_BLOCK
            , STR_DISPLAY
            , STR_NONE
            , STR_DEFAULT
            , STR_CUSTOM
            , STR_SELECTED
            , STR_CHECKED 
            
            , STATE_isBaseImportPage
            , STATE_baseImportList
            , STATE_customImportList } = constData;

    const { MakeOptionContainer
                , MakeOptionDeleteButton
                , MakeOptionPlusButton
                , MakeVpSuggestInputText_apiblock
                , MakeOptionInput } = baseComponent;
    /**
     * @param {Block} thatBlock Block
     * @param {string} optionPageSelector  Jquery 선택자
     */
    var InitImportBlockOption = function(thatBlock, optionPageSelector) {
        var uuid = thatBlock.getUUID();
        var blockContainerThis = thatBlock.getBlockContainerThis();
        var defaultImportContainer;
        var customImportContainer;
        var baseImportList = thatBlock.getState(STATE_baseImportList);
        var customImportList = thatBlock.getState(STATE_customImportList);
        
        /**
         * @event_function 
         */
        $(document).off(STR_CLICK, `.vp-apiblock-custom-import-plus-btn`);
        $(document).on(STR_CLICK, `.vp-apiblock-custom-import-plus-btn`, function(event) {

            var newData = {
                baseAcronyms : ''
                , baseImportName : 'numpy'
                , isImport : false
            }
            thatBlock.setState({
                customImportList: [ ...thatBlock.getState(STATE_customImportList), newData ]
            });
            var importCode = ShowImportListAtBlock(thatBlock);
            $(`.vp-block-header-${uuid}`).html(importCode);
            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });

        /**
         * default 옵션 클릭
         * @event_function 
         */
        $(document).off(STR_CLICK, `.vp-apiblock-default-option-${uuid}`);
        $(document).on(STR_CLICK, `.vp-apiblock-default-option-${uuid}`, function(event) {

            $(defaultImportContainer).css(STR_DISPLAY, STR_BLOCK);
            $(customImportContainer).css(STR_DISPLAY, STR_NONE);
            thatBlock.setState({
                isBaseImportPage: true
            });

            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });

        /**
         * detail 옵션 클릭
         * @event_function 
         */
        $(document).off(STR_CLICK, `.vp-apiblock-detail-option-${uuid}`);
        $(document).on(STR_CLICK, `.vp-apiblock-detail-option-${uuid}`, function(event) {

            $(customImportContainer).css(STR_DISPLAY, STR_BLOCK);
            $(defaultImportContainer).css(STR_DISPLAY, STR_NONE);
            thatBlock.setState({
                isBaseImportPage: false
            });
        
            blockContainerThis.renderBlockOptionTab();

            event.stopPropagation();
        });

        customImportList.forEach((customImportData, index) => {
            const { isImport, baseImportName, baseAcronyms } = customImportData;

            /**
             * @event_function 
             */
            $(document).off(STR_CLICK, `.vp-apiblock-blockoption-custom-import-input-${index}`);
            $(document).on(STR_CLICK, `.vp-apiblock-blockoption-custom-import-input-${index}`, function(event) {
                var _isImport = isImport === true ? false : true;
                var updatedData = {
                    baseAcronyms: thatBlock.getState(STATE_customImportList)[index].baseAcronyms
                    , baseImportName
                    , isImport: _isImport
                }
                thatBlock.setState({
                    customImportList: UpdateOneArrayValueAndGet(thatBlock.getState(STATE_customImportList), index, updatedData)
                });
                var importCode = ShowImportListAtBlock(thatBlock);
                $(`.vp-block-header-${uuid}`).html(importCode);
                blockContainerThis.renderBlockOptionTab();

                event.stopPropagation();
            });

            /**
             * @event_function 
             */
            $(document).off(STR_CHANGE, `.vp-apiblock-blockoption-custom-import-select-${index}`);
            $(document).on(STR_CHANGE, `.vp-apiblock-blockoption-custom-import-select-${index}`, function(event) {    
                var updatedData = {
                    baseAcronyms: thatBlock.getState(STATE_customImportList)[index].baseAcronyms
                    , baseImportName : $(STR_COLON_SELECTED, this).val()
                    , isImport
                }
                
                thatBlock.setState({
                    customImportList: UpdateOneArrayValueAndGet(thatBlock.getState(STATE_customImportList), index, updatedData)
                });
                var importCode = ShowImportListAtBlock(thatBlock);
                $(`.vp-block-header-${uuid}`).html(importCode);
                blockContainerThis.renderBlockOptionTab();

                event.stopPropagation();
            });

            /**
             * @event_function 
             */
            $(document).off(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-blockoption-custom-import-textinput-${index}`);
            $(document).on(STR_CHANGE_KEYUP_PASTE, `.vp-apiblock-blockoption-custom-import-textinput-${index}`, function(event) {
                RenderInputRequiredColor(this);

                var updatedData = {
                    baseAcronyms : $(this).val()
                    , baseImportName 
                    , isImport
                }
                thatBlock.setState({
                    customImportList: UpdateOneArrayValueAndGet(thatBlock.getState(STATE_customImportList), index, updatedData)
                });
                var importCode = ShowImportListAtBlock(thatBlock);
                $(`.vp-block-header-${uuid}`).html(importCode);
                event.stopPropagation();
            });
        });
        
        baseImportList.forEach((_, index) => {

           /**
            * @event_function 
            */
            $(document).off(STR_CLICK, `.vp-apiblock-blockoption-default-import-input-${index}`);
            $(document).on(STR_CLICK, `.vp-apiblock-blockoption-default-import-input-${index}`, function(event) {
                var isImport = thatBlock.getState(STATE_baseImportList)[index].isImport;
                var baseImportName = thatBlock.getState(STATE_baseImportList)[index].baseImportName;
                var baseAcronyms = thatBlock.getState(STATE_baseImportList)[index].baseAcronyms;

                isImport = isImport === true ? false : true;
                var updatedData = {
                    isImport
                    , baseImportName
                    , baseAcronyms
                }
                thatBlock.setState({
                    baseImportList: UpdateOneArrayValueAndGet(thatBlock.getState(STATE_baseImportList), index, updatedData)
                });
                var importCode = ShowImportListAtBlock(thatBlock);
                $(`.vp-block-header-${uuid}`).html(importCode);
                blockContainerThis.renderBlockOptionTab();

                event.stopPropagation();
            }); 
        });

        var RenderDefaultOrCustomImportContainer = function(importType, countisImport) {
            var name = STR_NULL;
            var customImportButton = STR_NULL;
            if (importType == IMPORT_BLOCK_TYPE.DEFAULT) {
                name = STR_DEFAULT;
            } else {
                name = STR_CUSTOM;
                customImportButton = MakeOptionPlusButton('', ' + import', 'vp-apiblock-custom-import-plus-btn');
                customImportButton = customImportButton.toString();
            }
        
            var container = $(`<div class='vp-apiblock-blockoption-${name}-import-container'>
                                    <div class='vp-apiblock-tab-navigation-node-block-title'>
                                        <span class='vp-block-optiontab-name
                                                     vp-apiblock-style-flex-column-center'>${name}</span>
                                        <div class='vp-apiblock-style-flex-row-center'>
                                            <span class='vp-apiblock-${name}-import-number
                                                         vp-apiblock-style-flex-column-center'
                                                    style='margin-right:5px;'>
                                                    ${countisImport} Selected
                                            </span>
                                                ${customImportButton}
                                           
                                        </div>
                                    </div>
                                </div>`);
     
            return container;
        }

        var RenderDefaultImportDom = function(baseImportData, index) {
            const { isImport, baseImportName, baseAcronyms } = baseImportData;
            var defaultImportDom = $(`<div class='vp-apiblock-style-flex-row-between'
                                            style='padding: 0.1rem 0;
                                                   margin-top:5px;'>
                                            <div class='vp-apiblock-style-flex-column-center'>
                                                <label class='vp-apiblock-style-flex-column-center'>
                                                    <input class='vp-apiblock-blockoption-default-import-input-${index}'
                                                            type='checkbox'
                                                            ${isImport == true 
                                                                ? 'checked'
                                                                : ''}>
                                                    </input>             
                                                    <span style='margin-top: -7px;'>
                                                    </span>
                                                </label>
             
                                            </div>
                                            <div class='vp-apiblock-style-flex-column-center'>
                                                <span style='font-size:12px; font-weight:700;'> ${baseImportName}</span>
                                            </div>
                                            <div class='vp-apiblock-style-flex-column-center'
                                                style='width: 50%;     text-align: center;'>
                                                <span class=''>${baseAcronyms}</span>
                                    
                                            </div>
                                    </div>`);
            return defaultImportDom;
        }

        var RenderDefaultOrDetailButton = function(thatBlock, uuid, blockCodeLineType) {
            var defaultOptionTitle = 'Default Import';
            var detailOptionTitle = 'Custom Import';
            // if (blockCodeLineType == BLOCK_CODELINE_TYPE.IMPORT) {
            //     defaultOptionTitle = `Default Import`;
            //     detailOptionTitle = `Custom Import`;
            // } else {
            //     defaultOptionTitle = `Default Option`;
            //     detailOptionTitle = `Detail Option`; 
            // }
     
            var isBaseImportPage = thatBlock.getState('isBaseImportPage');
            var defaultOrDetailButton = $(`<div class='vp-apiblock-style-flex-row-between'
                                                style='margin-top:5px;'>
     
                                                <button class='vp-apiblock-default-option-${uuid} 
                                                               vp-apiblock-default-detail-option-btn
                                                               ${isBaseImportPage == true ? 
                                                                    'vp-apiblock-option-btn-selected': 
                                                                    ''}'>
                                                        ${defaultOptionTitle}
                                                </button>
     
                                                <button class='vp-apiblock-detail-option-${uuid} 
                                                               vp-apiblock-default-detail-option-btn
                                                               ${isBaseImportPage == false 
                                                                    ? 'vp-apiblock-option-btn-selected': 
                                                                    ''}'>
                                                        ${detailOptionTitle}
                                                </button>
                                            </div>`);
            return defaultOrDetailButton;
        }
        var RenderCustomImportDom = function(customImportData, index) {
            const { isImport, baseImportName, baseAcronyms } = customImportData;
            var customImportDom = $(`<div class='vp-apiblock-style-flex-row-between'
                                          style='margin-top:5px;'>
     
                                        <div class='vp-apiblock-style-flex-column-center'>
                                            <label class='vp-apiblock-style-flex-column-center'>
                                                <input class='vp-apiblock-blockoption-custom-import-input
                                                            vp-apiblock-blockoption-custom-import-input-${index}' 
                                                    
                                                    type='checkbox' 
                                                    ${isImport == true ? STR_CHECKED: ''}>
                                                </input>
                                                <span style='margin-top: -7px;'>
                                                </span>
                                            </label>
                                        </div>
     
                                        <select class='vp-apiblock-select
                                                        vp-apiblock-blockoption-custom-import-select
                                                        vp-apiblock-blockoption-custom-import-select-${index}'
                                                style='margin-right:5px;'>
                                            <option value='numpy' ${baseImportName == 'numpy' ? STR_SELECTED : ''}>
                                                numpy
                                            </option>
                                            <option value='pandas' ${baseImportName == 'pandas' ? STR_SELECTED : ''}>
                                                pandas
                                            </option>
                                            <option value='matplotlib' ${baseImportName == 'matplotlib' ? STR_SELECTED : ''}>
                                                matplotlib
                                            </option>
                                            <option value='seaborn' ${baseImportName == 'seaborn' ? STR_SELECTED : ''}>
                                                seaborn
                                            </option>
                                            <option value='os' ${baseImportName == 'os' ? STR_SELECTED : ''}>
                                                os
                                            </option>
                                            <option value='sys' ${baseImportName == 'sys' ? STR_SELECTED : ''}>
                                                sys
                                            </option>
                                            <option value='time' ${baseImportName == 'time' ? STR_SELECTED : ''}>
                                                time
                                            </option>
                                            <option value='datetime' ${baseImportName == 'datetime' ? STR_SELECTED : ''}>
                                                datetime
                                            </option>
                                            <option value='random' ${baseImportName == 'random' ? STR_SELECTED : ''}>
                                                random
                                            </option>
                                            <option value='math' ${baseImportName == 'math' ? STR_SELECTED : ''}>
                                                math
                                            </option>
                                        </select>
     
                                        <div class='vp-apiblock-style-flex-column-center'>
                                            <input class='vp-apiblock-blockoption-custom-import-textinput
                                                          vp-apiblock-blockoption-custom-import-textinput-${index}
                                                        ${baseAcronyms == '' 
                                                            ? 'vp-apiblock-option-input-required' 
                                                            : ''}'
                                                    style='width: 90%;' 
                                                    type='text' 
                                                    placeholder='input import'
                                                    value='${baseAcronyms}'></input>
                                        </div>
     
                                    </div>`);
            return customImportDom;
        }
        /** Import option 렌더링 */
        var renderThisComponent = function() {
            var uuid = thatBlock.getUUID();
            var baseImportList = thatBlock.getState(STATE_baseImportList);

            var importBlockOption = MakeOptionContainer();
            var defaultOrDetailButton = RenderDefaultOrDetailButton(thatBlock, uuid, BLOCK_CODELINE_TYPE.IMPORT);
  
            importBlockOption.append(defaultOrDetailButton);

            /* ------------- import -------------- */
            var countisImport = 0;
            baseImportList.forEach(baseImportData => {
                if (baseImportData.isImport == true ) {
                    countisImport += 1;
                };
            });

            defaultImportContainer = RenderDefaultOrCustomImportContainer(IMPORT_BLOCK_TYPE.DEFAULT, countisImport);
            var defaultImportBody = $('<div><div>');
            baseImportList.forEach((baseImportData, index) => {
                var defaultImportDom = RenderDefaultImportDom(baseImportData, index);
                defaultImportBody.append(defaultImportDom);                        
            });

            /** -------------custom import ------------------ */
            var customImportList = thatBlock.getState(STATE_customImportList);
            var countIsCustomImport = 0;
            customImportList.forEach(baseImportData => {
                if (baseImportData.isImport == true ) {
                    countIsCustomImport += 1;
                };
            });

            // customImport 갯수만큼 bottom block 옵션에 렌더링
            customImportContainer = RenderDefaultOrCustomImportContainer(IMPORT_BLOCK_TYPE.CUSTOM, countIsCustomImport);
            var customImportBody = $(`<div class='vp-apiblock-customimport-body'>
                                    </div>`);
            customImportList.forEach((customImportData, index ) => {
                var customImportDom = RenderCustomImportDom(customImportData, index);
    ;
                var deleteButton = MakeOptionDeleteButton(index + uuid);
                $(deleteButton).click(function() {
                    thatBlock.setState({
                        customImportList: DeleteOneArrayValueAndGet(thatBlock.getState(STATE_customImportList), index)
                    });
                    
                    blockContainerThis.renderBlockOptionTab();
                });
                customImportDom.append(deleteButton);
                customImportBody.append(customImportDom);
            });

            var isBaseImportPage = thatBlock.getState(STATE_isBaseImportPage);
            if (isBaseImportPage == true) {
                defaultImportContainer.append(defaultImportBody);
                importBlockOption.append(defaultImportContainer);
            } else {
                customImportContainer.append(customImportBody);
                importBlockOption.append(customImportContainer);
            }
        
            $(optionPageSelector).append(importBlockOption);

            return importBlockOption;
        }

        return renderThisComponent();
    }

    return InitImportBlockOption;
});