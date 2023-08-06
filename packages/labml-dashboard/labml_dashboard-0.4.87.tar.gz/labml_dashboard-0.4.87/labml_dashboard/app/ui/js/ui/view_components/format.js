define(["require", "exports"], function (require, exports) {
    "use strict";
    Object.defineProperty(exports, "__esModule", { value: true });
    function numberWithCommas(x) {
        const parts = x.split('.');
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        return parts.join('.');
    }
    function formatScalar(value) {
        let str = value.toFixed(2);
        if (str.length <= 10) {
            str = value.toPrecision(10);
        }
        return numberWithCommas(str);
    }
    exports.formatScalar = formatScalar;
    function formatFixed(value, decimals) {
        let str = value.toFixed(decimals);
        return numberWithCommas(str);
    }
    exports.formatFixed = formatFixed;
    function formatInt(value) {
        if (value == null) {
            return '-';
        }
        let str = value.toString();
        return numberWithCommas(str);
    }
    exports.formatInt = formatInt;
    function formatSize(size) {
        let units = ['B', 'KB', 'MB', 'GB'];
        let unit = 'TB';
        for (let p of units) {
            if (size < 1024) {
                unit = p;
                break;
            }
            size /= 1024;
        }
        return ($) => {
            $('span.size', size.toFixed(2));
            $('span.size_unit', unit);
        };
    }
    exports.formatSize = formatSize;
    function formatValueWithBuilder(value, $) {
        if (typeof value === 'boolean') {
            let str = value.toString();
            $('span.boolean', str);
        }
        else if (typeof value === 'number') {
            if (value - Math.floor(value) < 1e-9) {
                let str = formatInt(value);
                $('span.int', str);
            }
            else {
                let str = formatInt(value);
                $('span.float', str);
            }
        }
        else if (typeof value === 'string') {
            $('span.string', value);
        }
        else if (value instanceof Array) {
            $('span.subtle', "[");
            for (let i = 0; i < value.length; ++i) {
                if (i > 0) {
                    $('span.subtle', ', ');
                }
                formatValueWithBuilder(value[i], $);
            }
            $('span.subtle', "]");
        }
        else {
            $('span.unknown', `${value}`);
        }
    }
    function formatValue(value) {
        return ($) => {
            formatValueWithBuilder(value, $);
        };
    }
    exports.formatValue = formatValue;
});
