define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
    , '../../api.js'    
    , '../../api_list.js'  
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'
], function ( $, vpCommon, vpConst, sb, vpSuggestInputText, api, api_list,
              constData, blockRenderer, baseComponent ) {

    const {  RenderInputRequiredColor
            , GenerateReturnOutParamList
            , ShowCodeBlockCode } = blockRenderer;

    const { STR_CHANGE_KEYUP_PASTE
            , STATE_codeLine } = constData;

    var InitTextBlockOption = function(thatBlock, optionPageSelector) {
        var importPakageUUID = thatBlock.getImportPakage().uuid;
        /**
            *  @event_function
            *  code 변경 이벤트 함수 
        */
       
        // VP_ID_APIBLOCK_OPTION_CODE_ARG
        $(document).off(STR_CHANGE_KEYUP_PASTE, vpCommon.formatString(".{0} #{1}{2}", importPakageUUID, vpConst.VP_ID_PREFIX, "markdownEditor"));
        $(document).on(STR_CHANGE_KEYUP_PASTE, vpCommon.formatString(".{0} #{1}{2}", importPakageUUID, vpConst.VP_ID_PREFIX, "markdownEditor"), function(event) {
            RenderInputRequiredColor(this);
            var inputValue = $(this).val();
            thatBlock.setState({
                [STATE_codeLine]: inputValue
            });

            event.stopPropagation();
        });

        /** Code option 렌더링 */
        var renderThisComponent = function() {

            var blockOptionPageDom = thatBlock.getBlockOptionPageDom();
            $(optionPageSelector).append(blockOptionPageDom);
            return blockOptionPageDom;
        }

        return renderThisComponent();
    }

    return InitTextBlockOption;
});