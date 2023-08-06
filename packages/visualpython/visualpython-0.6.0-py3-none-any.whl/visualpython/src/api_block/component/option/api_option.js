
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
    
    , '../../api.js'    
    , '../../constData.js'
    , '../../blockRenderer.js'
    , '../base/index.js'

], function ( $, vpCommon, vpConst, sb, xmlHandler, vpAccordionBox, vpLineNumberTextArea,vpIconInputText, vpFuncJS

              , api
        
              , constData
              , blockRenderer

              , baseComponent ) {

    const { SetTextareaLineNumber_apiBlock } = api;
 
    const { RenderInputRequiredColor
            , RenderCodeBlockInputRequired } = blockRenderer;

    const { BLOCK_CODELINE_TYPE
            , STR_CHANGE_KEYUP_PASTE

            , STR_NULL
            , STR_ONE_SPACE 
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_INPUT_YOUR_CODE
            , STR_COLOR

            , STATE_codeLine
            , COLOR_BLACK
            , COLOR_GRAY_input_your_code

            , VP_ID_PREFIX
            , VP_ID_APIBLOCK_OPTION_CODE_ARG

            , VP_CLASS_PREFIX
            , VP_CLASS_APIBLOCK_BOTTOM_TAB_VIEW
            , VP_CLASS_APIBLOCK_OPTION_INPUT_REQUIRED
            , VP_CLASS_APIBLOCK_BLOCK_HEADER } = constData;
    const { MakeOptionContainer } = baseComponent;

    /**
     * @param {Block} thatBlock Block
     * @param {string} optionPageSelector  Jquery 선택자
     */
    const InitCodeBlockOption = function(thatBlock, optionPageSelector) {
        /** Code option 렌더링 */
        const renderThisComponent = function() {
            var blockOptionPageDom = thatBlock.getBlockOptionPageDom();
            $(optionPageSelector).append(blockOptionPageDom);
            return blockOptionPageDom;
        }

        return renderThisComponent();
    }

    return InitCodeBlockOption;
});