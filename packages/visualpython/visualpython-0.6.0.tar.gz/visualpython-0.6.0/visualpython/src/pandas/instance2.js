define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/pandas/common/commonPandas'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
    , 'nbextensions/visualpython/src/common/vpBoard'
    , 'nbextensions/visualpython/src/common/component/vpSuggestInputText'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, libPandas, pdGen, VpBoard, vpSuggestInputText) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Instance2"
        , funcID : "pd_instance2"
        , libID : "pd000"
    }

    var vpBoardLeft;
    var vpBoardRight;

    var selectedBoard;

    //////////////// FIXME: move to constants file: Data Types constant ///////////////////////

    var _DATA_TYPES_OF_INDEX = [
        // Index 하위 유형
        'RangeIndex', 'CategoricalIndex', 'MultiIndex', 'IntervalIndex', 'DatetimeIndex', 'TimedeltaIndex', 'PeriodIndex', 'Int64Index', 'UInt64Index', 'Float64Index'
    ]

    var _DATA_TYPES_OF_GROUPBY = [
        // GroupBy 하위 유형
        'DataFrameGroupBy', 'SeriesGroupBy'
    ]

    var _SEARCHABLE_DATA_TYPES = [
        // pandas 객체
        'DataFrame', 'Series', 'Index', 'Period', 'GroupBy', 'Timestamp'
        , ..._DATA_TYPES_OF_INDEX
        , ..._DATA_TYPES_OF_GROUPBY
        // Plot 관련 유형
        //, 'Figure', 'AxesSubplot'
        // Numpy
        //, 'ndarray'
        // Python 변수
        //, 'str', 'int', 'float', 'bool', 'dict', 'list', 'tuple'
    ];

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback, meta) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM))).find(vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE)).addClass(uuid);

            // 옵션 객체 생성
            var varPackage = new VariablePackage(uuid);
            varPackage.metadata = meta;

            // 옵션 속성 할당.
            varPackage.setOptionProp(funcOptProp);
            // html 설정.
            varPackage.initHtml();
            callback(varPackage);  // 공통 객체를 callback 인자로 전달

            vpBoardLeft = new VpBoard(varPackage, '#vp_leftInstance');
            vpBoardLeft.load();

            // vpBoardRight = new VpBoard(varPackage, '#vp_rightInstance');
            // vpBoardRight.load();

            selectedBoard = vpBoardLeft;
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var initOption = function(callback, meta) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_GREEN_ROOM)), "pandas/instance2.html", optionLoadCallback, callback, meta);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var VariablePackage = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.package = {
            input: [
                { name: 'vp_varList' },
                { name: 'vp_colMeta' },
                { name: 'vp_returnType' },
                { name: 'vp_varApiSearch' },
                { name: 'vp_varApiFuncId' },
                { name: 'vp_returnVariable' }
            ]
        }

        // api list for variable
        // FIXME:
        this.apiList = {
            DataFrame: [
                { name: 'pandas.DataFrame.index', code: 'index' },
                { name: 'pandas.DataFrame.columns', code: 'columns' },
                { name: 'pandas.DataFrame.dtypes', code: 'dtypes' },
                { name: 'pandas.DataFrame.select_dtypes', code: 'select_dtypes()' },
                { name: 'pandas.DataFrame.values', code: 'values' },
                { name: 'pandas.DataFrame.shape', code: 'shape' },
                { name: 'pandas.DataFrame.head', code: 'head()' },
                { name: 'pandas.DataFrame.loc[]', code: 'loc[]' },
                { name: 'pandas.DataFrame.iloc[]', code: 'iloc[]' },
                { name: 'pandas.DataFrame.items', code: 'items()' },
                { name: 'pandas.DataFrame.keys', code: 'keys()' },
                { name: 'pandas.DataFrame.tail', code: 'tail()' },
                { name: 'pandas.DataFrame.where', code: 'where()' },
                { name: 'pandas.DataFrame.add', code: 'add()' },
                { name: 'pandas.DataFrame.sub', code: 'sub()' },
                { name: 'pandas.DataFrame.mul', code: 'mul()' },
                { name: 'pandas.DataFrame.div', code: 'div()' },
                { name: 'pandas.DataFrame.all', code: 'all()' },
                { name: 'pandas.DataFrame.any', code: 'any()' },
                { name: 'pandas.DataFrame.count', code: 'count()' },
                { name: 'pandas.DataFrame.describe', code: 'describe()' },
                { name: 'pandas.DataFrame.max', code: 'max()' },
                { name: 'pandas.DataFrame.mean', code: 'mean()' },
                { name: 'pandas.DataFrame.min', code: 'min()' },
                { name: 'pandas.DataFrame.sum', code: 'sum()' },
                { name: 'pandas.DataFrame.std', code: 'std()' },
                { name: 'pandas.DataFrame.drop', code: 'drop()' },
                { name: 'pandas.DataFrame.drop_duplicates', code: 'drop_duplicates()' },
                { name: 'pandas.DataFrame.dropna', code: 'dropna()' },
                { name: 'pandas.DataFrame.fillna', code: 'fillna()' },
                { name: 'pandas.DataFrame.isna', code: 'isna()' },
                { name: 'pandas.DataFrame.isnull', code: 'isnull()' },
                { name: 'pandas.DataFrame.notna', code: 'notna()' },
                { name: 'pandas.DataFrame.notnull', code: 'notnull()' },
                { name: 'pandas.DataFrame.replace', code: 'replace()' },
                { name: 'pandas.DataFrame.T', code: 'T' }
            ],
            Series: [
                { name: 'pandas.Series.index', code: 'index' },
                { name: 'pandas.Series.array', code: 'array' },
                { name: 'pandas.Series.values', code: 'values' },
                { name: 'pandas.Series.dtype', code: 'dtype' },
                { name: 'pandas.Series.shape', code: 'shape()' },
                { name: 'pandas.Series.size', code: 'size()' },
                { name: 'pandas.Series.T', code: 'T' },
                { name: 'pandas.Series.unique', code: 'unique()' },
                { name: 'pandas.Series.value_counts', code: 'value_counts()' },
                { name: 'pandas.Series.hasnans', code: 'hasnans' },
                { name: 'pandas.Series.dtypes', code: 'dtypes' },
                { name: 'pandas.Series.loc[]', code: 'loc[]' },
                { name: 'pandas.Series.iloc[]', code: 'iloc[]' },
                { name: 'pandas.Series.items', code: 'items()' },
                { name: 'pandas.Series.keys', code: 'keys()' },
                { name: 'pandas.Series.add', code: 'add()' },
                { name: 'pandas.Series.sub', code: 'sub()' },
                { name: 'pandas.Series.mul', code: 'mul()' },
                { name: 'pandas.Series.div', code: 'div()' },
                { name: 'pandas.Series.all', code: 'all()' },
                { name: 'pandas.Series.any', code: 'any()' },
                { name: 'pandas.Series.count', code: 'count()' },
                { name: 'pandas.Series.describe', code: 'describe()' },
                { name: 'pandas.Series.max', code: 'max()' },
                { name: 'pandas.Series.mean', code: 'mean()' },
                { name: 'pandas.Series.min', code: 'min()' },
                { name: 'pandas.Series.sum', code: 'sum()' },
                { name: 'pandas.Series.std', code: 'std()' },
                { name: 'pandas.Series.drop', code: 'drop()' },
                { name: 'pandas.Series.drop_duplicates', code: 'drop_duplicates()' },
                { name: 'pandas.Series.dropna', code: 'dropna()' },
                { name: 'pandas.Series.fillna', code: 'fillna()' },
                { name: 'pandas.Series.isna', code: 'isna()' },
                { name: 'pandas.Series.isnull', code: 'isnull()' },
                { name: 'pandas.Series.notna', code: 'notna()' },
                { name: 'pandas.Series.notnull', code: 'notnull()' },
                { name: 'pandas.Series.replace', code: 'replace()' },
                { name: 'pandas.Series.map', code: 'map(lambda p: p)' }
            ]
        }
    }



    /**
     * vpFuncJS 에서 상속
     */
    VariablePackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    VariablePackage.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }

    VariablePackage.prototype.getMetadata = function(id) {
        if (this.metadata == undefined)
            return "";
        var len = this.metadata.options.length;
        for (var i = 0; i < len; i++) {
            var obj = this.metadata.options[i];
            if (obj.id == id)
                return obj.value;
        }
        return "";
    }

    VariablePackage.prototype.getMetaLoaded = function(id) {
        if (this.metadata == undefined)
            return true;

        var result = true;
        var len = this.metadata.options.length;
        for (var i = 0; i < len; i++) {
            var obj = this.metadata.options[i];
            if (obj.id == id)
            {
                if (obj.metaLoaded != true) {
                    result = false;
                }
                break;
            }
        }
        return result;
    }

    VariablePackage.prototype.checkMetaLoaded = function(id) {
        if (this.metadata == undefined)
            return true;
        var len = this.metadata.options.length;
        for (var i = 0; i < len; i++) {
            if (this.metadata.options[i].id == id) {
                this.metadata['options'][i]['metaLoaded'] = true;
            }
        }
        return true;
    }

    /**
     * html 내부 binding 처리
     */
    VariablePackage.prototype.initHtml = function() {
        var that = this;

        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/commonPandas.css");
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/instance2.css");

        this.showFunctionTitle();

        this.getVariableDir();

        // hide del-col button & connect operator tag as default
        $(this.wrapSelector('.vp-oper-connect')).hide();

        // Clear Board
        $(this.wrapSelector('#vp_instanceClear')).click(function() {
            selectedBoard.clear();

            // search again
            that.getVariableDir();
        });

        // Backspace
        $(this.wrapSelector('#vp_instanceBackspace')).click(function() {
            selectedBoard.removeBlock(selectedBoard.getLastBlockKey());

            // search again
            that.getVariableDir(selectedBoard.getCode());
        });

        // Board 클릭 시
        $(this.wrapSelector('.vp-instance-box')).click(function() {
            $(that.wrapSelector('.vp-instance-box')).removeClass('selected');
            $(this).addClass('selected');
            if ($(this).hasClass('left')) {
                selectedBoard = vpBoardLeft;
            } else {
                selectedBoard = vpBoardRight;
            }
        });

        // Attribute, Method 변경 시
        $(this.wrapSelector('.vp-instance-search')).change(function() {
            var varName = $(this).val();
            var blockType = $(this).hasClass('attr')? 'var': 'api';

            if (selectedBoard.getBoardSize() > 0) {
                varName = '.' + varName;
            }

            selectedBoard.addBlocks([{
                code: varName,
                type: blockType
            }]);

            // reset search tag
            $(that.wrapSelector('.vp-instance-search')).val('');

            // refresh with dir
            that.getVariableDir(selectedBoard.getCode());
        });

        // Attribute 클릭 시
        $(document).on('click', this.wrapSelector('#vp_insAttr ul li'), function() {
            var varName = $(this).attr('data-var-name');

            $(that.wrapSelector('#vp_insAttrSearch')).val(varName);
            $(that.wrapSelector('#vp_insAttrSearch')).change();
        });

        // Method 클릭 시
        $(document).on('click', this.wrapSelector('#vp_insMethod ul li'), function() {
            var varName = $(this).attr('data-var-name');

            $(that.wrapSelector('#vp_insMethodSearch')).val(varName);
            $(that.wrapSelector('#vp_insMethodSearch')).change();
        });

        // column selection
        $(document).on('change', this.wrapSelector('.vp-col-list'), function() {
            that.replaceBoard();

            var objName = $(that.wrapSelector('#vp_varList')).val();
            var colName = $(this).val();
            var colDtype = $(this).find(':selected').data('dtype');
            var conditionTag = $(this).closest('td').find('.vp-condition');

            if (colDtype == 'object') {
                // search column unique values
                var code = new sb.StringBuilder();
                code.appendLine('import json');
                code.appendFormatLine('_vpcoluniq = {0}[{1}].unique()', objName, convertToStr(colName));
                code.appendLine('_vpcoluniq.sort()');
                // code.append('print(json.dumps(list(_vpcoluniq)))');
                code.append(`print(json.dumps([ { "value": ("'" + c + "'") if type(c).__name__ == 'str' else c, "label": c } for c in list(_vpcoluniq) ]))`);
                that.kernelExecute(code.toString(), function(result) {
                    var varResult = JSON.parse(result);
                    
                    if (varResult != undefined && varResult.length > 0) {
                        // conditions using suggestInput
                        var suggestInput = new vpSuggestInputText.vpSuggestInputText();
                        suggestInput.addClass('vp-input m');
                        suggestInput.addClass('vp-condition');
                        suggestInput.setPlaceholder("categorical dtype");
                        suggestInput.setSuggestList(function() { return varResult; });
                        suggestInput.setSelectEvent(function(value) {
                            $(this.wrapSelector()).val(value);
                            that.replaceBoard();
                        });
                        suggestInput.setNormalFilter(false);
                        $(conditionTag).replaceWith(function() {
                            return suggestInput.toTagString();
                        });
                    }
                });
            } else {
                // condition reset using suggestInput
                var suggestInput = new vpSuggestInputText.vpSuggestInputText();
                suggestInput.addClass('vp-input m');
                suggestInput.addClass('vp-condition');
                if (colDtype != undefined) {
                    suggestInput.setPlaceholder(colDtype + " dtype");
                }
                suggestInput.setNormalFilter(false);
                $(conditionTag).replaceWith(function() {
                    return suggestInput.toTagString();
                });
            }

        });
        // operator selection
        $(document).on('click', this.wrapSelector('.vp-oper-list'), function() {
            that.replaceBoard();
        });
        // condition change
        $(document).on('change', this.wrapSelector('.vp-condition'), function() {
            that.replaceBoard();
        });
        // connector selection
        $(document).on('click', this.wrapSelector('.vp-oper-connect'), function() {
            that.replaceBoard();
        });

        // on column add
        $(this.wrapSelector('#vp_addCol')).click(function() {
            var clone = $(that.wrapSelector('#vp_colList tr:first')).clone();

            clone.find('input').val('');
            clone.find('.vp-condition').attr({'placeholder': ''});
            // hide last connect operator
            clone.find('.vp-oper-connect').hide();
            // show connect operator right before last one
            $(that.wrapSelector('#vp_colList .vp-oper-connect:last')).show();
            clone.insertBefore('#vp_colList tr:last');

            // show delete button
            // $(that.wrapSelector('#vp_colList tr td .vp-del-col')).show();
        });
        // on column delete
        $(document).on("click", this.wrapSelector('.vp-del-col'), function(event) {
            event.stopPropagation();
            
            var colList = $(that.wrapSelector('#vp_colList tr td:not(:last)'));
            if (colList.length <= 1) {
                // clear
                $(that.wrapSelector('.vp-col-list')).val('');
                $(that.wrapSelector('.vp-oper-list')).val('');
                $(that.wrapSelector('.vp-condition')).val('');
                $(that.wrapSelector('.vp-condition')).attr({ 'placeholder': '' });
                $(that.wrapSelector('.vp-oper-connect')).val('');
            } else {
                $(this).parent().parent().remove();
                $(that.wrapSelector('#vp_colList .vp-oper-connect:last')).hide();

                if (colList.length == 2) {
                    if ($(that.wrapSelector('.vp-col-list')).val() != '') {
                        $(that.wrapSelector('#vp_returnType')).attr('disabled', false);
                    }
                }
            }

            that.replaceBoard();
        });

        // on return type change
        $(this.wrapSelector('#vp_returnType')).change(function() {
            that.replaceBoard();

            $(that.wrapSelector('#vp_varApiSearch')).val('');
            $(that.wrapSelector('#vp_varApiFuncId')).val('');

            // load API List for selected variable
            that.loadApiList();
        });
    }

    VariablePackage.prototype.getVariableDir = function(varName = '', callback = undefined) {
        var that = this;

        // remove brackets
        varName = varName.replace(/[()]/g, '');

        var code = new sb.StringBuilder();
        code.appendLine('import json');
        code.appendFormatLine('_vp_vars = dir({0})', varName);
        code.append('print(json.dumps(');
        if (varName == '') {
            code.append("{ 'type': 'None', 'list': [");
            code.append("{ 'name': v, 'type': type(eval(v)).__name__ } ");
        } else {
            code.appendFormat("{ 'type': type({0}).__name__, 'list': [", varName);
            code.appendFormat("{ 'name': v, 'type': type(eval('{0}.' + v)).__name__ } ", varName);
        }
        code.appendFormat(" for v in _vp_vars if (not v.startswith('_')) and (v not in {0})"
                        , JSON.stringify(pdGen._VP_NOT_USING_VAR));
        code.appendLine(']}))');
        var codes = code.toString();
        this.kernelExecute(codes, function(result) {
            var varObj = JSON.parse(result);

            var varType = varObj.type;
            var varList = varObj.list;

            // set variable type
            $(that.wrapSelector('#vp_instanceType')).text(varType);

            // dir list
            var attrListTag = new sb.StringBuilder();
            var methodListTag = new sb.StringBuilder();
            var attrList = [];
            var methodList = [];
            varList != undefined && varList.forEach(obj => {
                if (obj.type == 'function' || obj.type == 'method' || obj.type == 'type') {
                    methodListTag.appendFormatLine('<li class="vp-select-item" data-var-name="{0}" data-var-type="{1}"><span>{2}</span>{3}</li>'
                                                , obj.name + '()', obj.type, obj.type, obj.name);
                    methodList.push({
                        label: obj.name + '()' + ' (' + obj.type + ')',
                        value: obj.name + '()' 
                    });
                } else {
                    attrListTag.appendFormatLine('<li class="vp-select-item" data-var-name="{0}" data-var-type="{1}"><span>{2}</span>{3}</li>'
                                                , obj.name, obj.type, obj.type, obj.name);
                    attrList.push({
                        label: obj.name + ' (' + obj.type + ')',
                        value: obj.name
                    });
                }

            });
            $(that.wrapSelector('#vp_insAttr ul')).html(attrListTag.toString());
            $(that.wrapSelector('#vp_insMethod ul')).html(methodListTag.toString());

            $(that.wrapSelector('#vp_insAttrSearch')).autocomplete({
                source : attrList
            });

            $(that.wrapSelector('#vp_insMethodSearch')).autocomplete({
                source : methodList
            });

            // show pandas object box
            // TODO: option box 오류 수정한 후에 적용
            // if (varType == 'DataFrame' || varType == 'Series') {
            //     $(that.wrapSelector('.vp-instance-option-box.object')).show();
            // } else {
            //     $(that.wrapSelector('.vp-instance-option-box.object')).hide();
            // }

        });
    }

    var convertToStr = function(code) {
        if (!$.isNumeric(code)) {
            code = `'${code}'`;
        }
        return code;
    }

    /**
     * make block to add on API Board
     */
    VariablePackage.prototype.makeBlock = function() {
        var varName = $(this.wrapSelector('#vp_varList')).find(':selected').attr('data-var-name');
        if (varName == undefined || varName == '') {
            return [];
        }

        var varType = $(this.wrapSelector('#vp_varList')).find(':selected').attr('data-var-type');

        var apiCode = $(this.wrapSelector('#vp_varApiSearch')).val();

        /**
         * Add block to board with condition
         * - type: var / api
         * - columns : column / condition(column + operator)
         * - return type : if last bracket has only one column - DataFrame/Series selectable
         *               / else - its datatype
         * - cases :
         *  1) df[col] / df[[col]] / df[[col1, col2]]
         *  2) df[condition] / df[condition1 & condition2]
         *  3) df[condition][col] / df[condition][[col]]
         *  4) df[[col]][condition]
         *  5) s
         */

        // vpBoard add
        var blocks = [
            { code: varName, type: 'var', next: -1 }
        ];

        // columns + condition block
        var colList = $(this.wrapSelector('#vp_colList tr td:not(:last)'));
        var colMeta = []; // metadata for column list
        
        var colSelector = [];   // temporary column list 
        var condSelector = [];  // temporary condition list
        for (var i = 0; i < colList.length; i++) {
            var colTag = $(colList[i]);
            var colName = colTag.find('.vp-col-list').val();
            var oper = colTag.find('.vp-oper-list').val();
            var cond = colTag.find('.vp-condition').val();
            var connector = i > 0? $(colList[i- 1]).find('.vp-oper-connect').val() : undefined;

            // if no column selected, pass
            if (colName == "") continue;

            // save metadata for column list
            colMeta.push({
                'vp-col-list': colName,
                'vp-oper-list': oper,
                'vp-condition': cond,
                'vp-oper-connect': $(colList[i]).find('.vp-oper-connect').val()
            });

            // if operator selected, condition / else column
            if (oper == '') {
                // column 
                // add blocks with last temp condition list
                if (condSelector.length > 0) {
                    // block result : [condition1, condition2]
                    var idx = blocks.length;
                    blocks = blocks.concat(condSelector);
                    var lastIdx = blocks.length - 1;
                    // [] 추가
                    blocks.push({
                        code: '[]', type: 'brac', child: lastIdx
                    });

                    // idx 연결
                    blocks[idx - 1]['next'] = blocks.length - 1;

                    condSelector = [];
                }
                // column selector
                colSelector.push(colName);
            } else {
                // condition selector
                // add blocks with last temp column list
                if (colSelector.length > 0) {
                    // block result : [[code1, code2]] / [[col]]
                    var idx = blocks.length;
                    blocks[idx - 1]['next'] = idx + 2;
                    blocks.push({
                        code: colSelector.map(v => convertToStr(v)).toString(),
                        type: 'code'
                    });
                    blocks.push({
                        code: '[]', type: 'brac', child: idx
                    });
                    blocks.push({
                        code: '[]', type: 'brac', child: idx + 1
                    });
                    
                    colSelector = [];
                }
                var idx = blocks.length + condSelector.length;
                var hasPrev = condSelector.length > 0;
                condSelector = condSelector.concat([
                    { code: varName, type: 'var', next: idx + 2 },     // idx
                    { code: convertToStr(colName), type: 'code' },    
                    { code: '[]', type: 'brac', child: idx + 1 }
                ]);
                if (cond != undefined && cond !== '') {
                    condSelector.push({ code: cond, type: 'code' });
                    condSelector.push({ code: oper, type: 'oper', left: idx, right: idx + 3 });
                } else {
                    condSelector.push({ code: oper, type: 'oper', left: idx, right: -1 });
                }
                if (connector != undefined && hasPrev) {
                    condSelector.push({
                        code: connector, type: 'oper'
                        , left: idx - 1
                        , right: blocks.length + condSelector.length - 1
                    });
                }
            }
        }

        if (condSelector.length > 0) {
            var idx = blocks.length;
            blocks = blocks.concat(condSelector);
            var lastIdx = blocks.length - 1;
            // [] 추가
            blocks.push({
                code: '[]', type: 'brac', child: lastIdx
            });

            // idx 연결
            blocks[idx - 1]['next'] = blocks.length - 1;

            condSelector = [];

            // only same as datatype
            $(this.wrapSelector('#vp_returnType')).val(varType);
            $(this.wrapSelector('#vp_returnType')).attr('disabled', true);
            // load API List for selected variable
            this.loadApiList();
        } else {
            // set return type depends on last columns
            if (colSelector.length != 1) {
                // only dataframe
                $(this.wrapSelector('#vp_returnType')).val(varType);
                $(this.wrapSelector('#vp_returnType')).attr('disabled', true);
                // load API List for selected variable
                this.loadApiList();
            } else {
                // allow dataframe/series selection
                $(this.wrapSelector('#vp_returnType')).attr('disabled', false);
            }

            var returnType = $(this.wrapSelector('#vp_returnType')).val();
            if (colSelector.length > 0) {
                if (returnType == 'DataFrame') {
                    // with double brackets
                    var idx = blocks.length;
                    blocks[idx - 1]['next'] = idx + 2;
                    blocks.push({
                        code: colSelector.map(v => convertToStr(v)).toString(),
                        type: 'code'
                    });
                    blocks.push({
                        code: '[]', type: 'brac', child: idx
                    });
                    blocks.push({
                        code: '[]', type: 'brac', child: idx + 1
                    });
                } else if (returnType == 'Series') {
                    // with single bracket
                    var idx = blocks.length;
                    blocks[idx - 1]['next'] = idx + 1;
                    blocks.push({
                        code: colSelector.map(v => convertToStr(v)).toString(),
                        type: 'code'
                    });
                    blocks.push({
                        code: '[]', type: 'brac', child: idx
                    });
                }
            }
            
        }

        // api list attach
        if (apiCode != undefined && apiCode != '') {
            blocks[blocks.length -1]['next'] = blocks.length;
            blocks.push({
                code: '.' + apiCode, type: 'api'
            })
        }

        // save column metadata
        $(this.wrapSelector('#vp_colMeta')).val(encodeURIComponent(JSON.stringify(colMeta)));

        return blocks;
    }

    /**
     * initialize options
     */
    VariablePackage.prototype.initOptions = function(loadMeta = false) {
        var that = this;

        // show api list
        $(this.wrapSelector('#vp_varApiSearch')).autocomplete({
            source: {},
            minLength: 2,
            autoFocus: true,
            select: function(event, ui) {
                $(that.wrapSelector('#vp_varApiSearch')).val(ui.item.value);
                $(that.wrapSelector('#vp_varApiFuncId')).val(ui.item.id);

                that.replaceBoard();
            },
            change: function(event, ui) {
                that.replaceBoard();
            }
        });

        if (loadMeta) {
            // load other metadata
            $(this.wrapSelector('#vp_returnType')).val(this.getMetadata('vp_returnType'));
            $(this.wrapSelector('#vp_apiSearch')).val(this.getMetadata('vp_apiSearch'));
            this.checkMetaLoaded('vp_returnType');
            this.checkMetaLoaded('vp_apiSearch');
        } else {
            $(this.wrapSelector('#vp_varApiSearch')).val('');
            $(this.wrapSelector('#vp_varApiFuncId')).val('');
        }

        // bind event for variable selection
        this.handleVariableSelection();
        // load API List for selected variable
        this.loadApiList();
        
    }

    /**
     * 선택한 패키지명 입력
     */
    VariablePackage.prototype.showFunctionTitle = function() {
        $(this.wrapSelector('.vp_functionName')).text(funcOptProp.funcName);
    }

    /**
     * refresh and replace board with current information
     * - variable + columns/conditions + return type + api
     */
    VariablePackage.prototype.replaceBoard = function() {
        // clear board
        selectedBoard.clear();
        // add block
        selectedBoard.addBlocks(this.makeBlock());
    }

    /**
     * Bind variable selection events
     * - on change variables
     */
    VariablePackage.prototype.handleVariableSelection = function() {
        // get selected variable info
        var varName = $(this.wrapSelector('#vp_insAttr .vp-select-item.selected')).data('var-name');
        var varType = $(this.wrapSelector('#vp_insAttr .vp-select-item.selected')).data('var-type');

        // initialize on event : hide options
        $(this.wrapSelector('#vp_colList')).closest('tr').hide();
        // initialize column list
        var clone = $(this.wrapSelector('#vp_colList tr:first')).clone();
        clone.find('input').val('');
        clone.find('.vp-condition').attr({'placeholder': ''});
        // hide last connect operator
        clone.find('.vp-oper-connect').hide();
        // hide delete button
        // clone.find('.vp-del-col').hide();

        $(this.wrapSelector('#vp_colList tr:not(:last)')).remove();
        $(this.wrapSelector('#vp_colList')).prepend(clone);

        // Pandas Objects
        // if pandas object
        if (varType == 'DataFrame') {
            // 2. DataFrame - show index, columns
            this.getObjectDetail(varName, 'columns', '.vp-col-list');

            $(this.wrapSelector('#vp_colList')).closest('tr').show();

            $(this.wrapSelector('#vp_returnType')).attr('disabled', false);

        } else if (varType == 'Series') {
            // series
            // replace board with now status of board option
            this.replaceBoard();

            $(this.wrapSelector('#vp_returnType')).attr('disabled', true);
        }
    };

    /**
     * Get variable detail
     * @param {string} varName 
     * @param {string} property 
     * @param {string} selectId select tag id with selector
     */
    VariablePackage.prototype.getObjectDetail = function(varName, property, selectId) {
        var that = this;
        // 변수 col, idx 정보 조회 command, callback
        var command = new sb.StringBuilder();
        command.appendLine('import json');
        command.append('print(json.dumps([ { "value": c ')
        if (property == 'columns') {
            command.appendFormat(', "dtype": str({0}[c].dtype)', varName);
        }
        command.appendFormat('} for c in {0}.{1} ]))', varName, property);
        this.kernelExecute(command.toString(), function(result) {
            var varList = JSON.parse(result);

            var optVar = new sb.StringBuilder();
            optVar.appendLine('<option value=""></option>');
            varList.forEach(obj => {
                optVar.appendFormat('<option value="{0}"', obj.value);
                if (property == 'columns') {
                    optVar.appendFormat(' data-dtype="{0}"', obj.dtype)
                }
                optVar.appendFormatLine('>{0}</option>', obj.value);
            });

            $(that.wrapSelector(selectId)).html(optVar.toString());

            // if first time loading, set with metadata
            if (that.getMetaLoaded('vp_colMeta') == false) {
                var decodedMeta = decodeURIComponent(that.getMetadata('vp_colMeta'));
                if (decodedMeta != "") {
                    var colMeta = JSON.parse(decodedMeta);
                    // add columns as colMeta length
                    for(var i = 0; i < colMeta.length -1; i++) {
                        $(that.wrapSelector('#vp_addCol')).trigger('click');
                    }
                    // load column data
                    var colList = $(that.wrapSelector('#vp_colList tr td:not(:last)'));
                    for (var i = 0; i < colList.length; i++) {
                        var colTag = $(colList[i]);
                        colTag.find('.vp-col-list').val(colMeta[i]['vp-col-list']);
                        colTag.find('.vp-oper-list').val(colMeta[i]['vp-oper-list']);
                        colTag.find('.vp-condition').val(colMeta[i]['vp-condition']);
                        colTag.find('.vp-oper-connect').val(colMeta[i]['vp-oper-connect']);
                    }
                }
                that.checkMetaLoaded('vp_colMeta');
            }

            // replace board with now status of board option
            that.replaceBoard();
        });      
    };

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    VariablePackage.prototype.generateCode = function(addCell, exec) {
        if (!this.optionValidation()) return;
        
        var sbCode = new sb.StringBuilder();

        // TODO: 변수 내용 조회
        var boardCode = selectedBoard.getCode();
        if (boardCode == undefined) return ""; // 코드 생성 중 오류 발생
        
        var returnCode = $(this.wrapSelector('#vp_returnVariable')).val();
        if (returnCode != '') {
            returnCode = returnCode + ' = ';
        }

        sbCode.appendFormat('{0}{1}', returnCode, boardCode);

        if (addCell) this.cellExecute(sbCode.toString(), exec);

        return sbCode.toString();
    }

    return {
        initOption: initOption
    };
});