(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2994],{9146:function(e,t,n){"use strict";n.d(t,{d:function(){return o}});var r=n(40095),o=function(e,t){return e&&e.attributes.supported_features?Object.keys(t).map((function(n){return(0,r.e)(e,Number(n))?t[n]:""})).filter((function(e){return""!==e})).join(" "):""}},81303:function(e,t,n){"use strict";n(8878);function r(e){return(r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function o(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function a(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function i(e,t,n){return(i="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=l(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(n):o.value}})(e,t,n||e)}function u(e,t){return(u=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function c(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=l(e);if(t){var o=l(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return s(this,n)}}function s(e,t){return!t||"object"!==r(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function l(e){return(l=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var p=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&u(e,t)}(p,e);var t,n,r,s=c(p);function p(){return o(this,p),s.apply(this,arguments)}return t=p,(n=[{key:"ready",value:function(){var e=this;i(l(p.prototype),"ready",this).call(this),setTimeout((function(){"rtl"===window.getComputedStyle(e).direction&&(e.style.textAlign="right")}),100)}}])&&a(t.prototype,n),r&&a(t,r),p}(customElements.get("paper-dropdown-menu"));customElements.define("ha-paper-dropdown-menu",p)},52994:function(e,t,n){"use strict";n.r(t);n(21157),n(53973),n(51095);var r=n(21683),o=n(78956),a=n(50856),i=n(28426),u=n(9146),c=n(40095),s=(n(81303),n(43709),n(10983),n(11052));function l(e){return(l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function p(){var e=function(e,t){t||(t=e.slice(0));return Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(['\n      <style include="iron-flex iron-flex-alignment"></style>\n      <style>\n        /* local DOM styles go here */\n        :host {\n          @apply --layout-flex;\n          @apply --layout-horizontal;\n          @apply --layout-justified;\n        }\n        .in-flux#target_temperature {\n          color: var(--error-color);\n        }\n        #target_temperature {\n          @apply --layout-self-center;\n          font-size: 200%;\n        }\n        .control-buttons {\n          font-size: 200%;\n          text-align: right;\n        }\n        ha-icon-button {\n          height: 48px;\n          width: 48px;\n        }\n      </style>\n\n      \x3c!-- local DOM goes here --\x3e\n      <div id="target_temperature">[[value]] [[units]]</div>\n      <div class="control-buttons">\n        <div>\n          <ha-icon-button\n            icon="hass:chevron-up"\n            on-click="incrementValue"\n          ></ha-icon-button>\n        </div>\n        <div>\n          <ha-icon-button\n            icon="hass:chevron-down"\n            on-click="decrementValue"\n          ></ha-icon-button>\n        </div>\n      </div>\n    ']);return p=function(){return e},e}function f(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function h(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function y(e,t){return(y=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function m(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=b(e);if(t){var o=b(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return d(this,n)}}function d(e,t){return!t||"object"!==l(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function b(e){return(b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}var v=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&y(e,t)}(i,e);var t,n,r,o=m(i);function i(){return f(this,i),o.apply(this,arguments)}return t=i,r=[{key:"template",get:function(){return(0,a.d)(p())}},{key:"properties",get:function(){return{value:{type:Number,observer:"valueChanged"},units:{type:String},min:{type:Number},max:{type:Number},step:{type:Number,value:1}}}}],(n=[{key:"temperatureStateInFlux",value:function(e){this.$.target_temperature.classList.toggle("in-flux",e)}},{key:"incrementValue",value:function(){var e=this.value+this.step;this.value<this.max&&(this.last_changed=Date.now(),this.temperatureStateInFlux(!0)),e<=this.max?e<=this.min?this.value=this.min:this.value=e:this.value=this.max}},{key:"decrementValue",value:function(){var e=this.value-this.step;this.value>this.min&&(this.last_changed=Date.now(),this.temperatureStateInFlux(!0)),e>=this.min?this.value=e:this.value=this.min}},{key:"valueChanged",value:function(){var e=this;this.last_changed&&window.setTimeout((function(){Date.now()-e.last_changed>=2e3&&(e.fire("change"),e.temperatureStateInFlux(!1),e.last_changed=null)}),2010)}}])&&h(t.prototype,n),r&&h(t,r),i}((0,s.I)(i.H3));function g(e){return(g="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function _(){var e=function(e,t){t||(t=e.slice(0));return Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(['\n      <style include="iron-flex"></style>\n      <style>\n        :host {\n          color: var(--primary-text-color);\n        }\n\n        ha-paper-dropdown-menu {\n          width: 100%;\n        }\n\n        paper-item {\n          cursor: pointer;\n        }\n\n        ha-water_heater-control.range-control-left,\n        ha-water_heater-control.range-control-right {\n          float: left;\n          width: 46%;\n        }\n        ha-water_heater-control.range-control-left {\n          margin-right: 4%;\n        }\n        ha-water_heater-control.range-control-right {\n          margin-left: 4%;\n        }\n\n        .single-row {\n          padding: 8px 0;\n        }\n        }\n      </style>\n\n      <div class$="[[computeClassNames(stateObj)]]">\n        <div class="container-temperature">\n          <div class$="[[stateObj.attributes.operation_mode]]">\n            <div hidden$="[[!supportsTemperatureControls(stateObj)]]">\n              [[localize(\'ui.card.water_heater.target_temperature\')]]\n            </div>\n            <template is="dom-if" if="[[supportsTemperature(stateObj)]]">\n              <ha-water_heater-control\n                value="[[stateObj.attributes.temperature]]"\n                units="[[hass.config.unit_system.temperature]]"\n                step="[[computeTemperatureStepSize(hass, stateObj)]]"\n                min="[[stateObj.attributes.min_temp]]"\n                max="[[stateObj.attributes.max_temp]]"\n                on-change="targetTemperatureChanged"\n              >\n              </ha-water_heater-control>\n            </template>\n          </div>\n        </div>\n\n        <template is="dom-if" if="[[supportsOperationMode(stateObj)]]">\n          <div class="container-operation_list">\n            <div class="controls">\n              <ha-paper-dropdown-menu\n                label-float=""\n                dynamic-align=""\n                label="[[localize(\'ui.card.water_heater.operation\')]]"\n              >\n                <paper-listbox\n                  slot="dropdown-content"\n                  selected="[[stateObj.attributes.operation_mode]]"\n                  attr-for-selected="item-name"\n                  on-selected-changed="handleOperationmodeChanged"\n                >\n                  <template\n                    is="dom-repeat"\n                    items="[[stateObj.attributes.operation_list]]"\n                  >\n                    <paper-item item-name$="[[item]]"\n                      >[[_localizeOperationMode(localize, item)]]</paper-item\n                    >\n                  </template>\n                </paper-listbox>\n              </ha-paper-dropdown-menu>\n            </div>\n          </div>\n        </template>\n\n        <template is="dom-if" if="[[supportsAwayMode(stateObj)]]">\n          <div class="container-away_mode">\n            <div class="center horizontal layout single-row">\n              <div class="flex">\n                [[localize(\'ui.card.water_heater.away_mode\')]]\n              </div>\n              <ha-switch\n                checked="[[awayToggleChecked]]"\n                on-change="awayToggleChanged"\n              >\n              </ha-switch>\n            </div>\n          </div>\n        </template>\n      </div>\n    ']);return _=function(){return e},e}function w(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function O(e,t){for(var n=0;n<t.length;n++){var r=t[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(e,r.key,r)}}function j(e,t){return(j=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function k(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=x(e);if(t){var o=x(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return S(this,n)}}function S(e,t){return!t||"object"!==g(t)&&"function"!=typeof t?function(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}(e):t}function x(e){return(x=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}customElements.define("ha-water_heater-control",v);var C=function(e){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&j(e,t)}(l,e);var t,n,i,s=k(l);function l(){return w(this,l),s.apply(this,arguments)}return t=l,i=[{key:"template",get:function(){return(0,a.d)(_())}},{key:"properties",get:function(){return{hass:{type:Object},stateObj:{type:Object,observer:"stateObjChanged"},awayToggleChecked:Boolean}}}],(n=[{key:"stateObjChanged",value:function(e,t){var n=this;e&&this.setProperties({awayToggleChecked:"on"===e.attributes.away_mode}),t&&(this._debouncer=o.d.debounce(this._debouncer,r.Wc.after(500),(function(){n.fire("iron-resize")})))}},{key:"computeTemperatureStepSize",value:function(e,t){return t.attributes.target_temp_step?t.attributes.target_temp_step:-1!==e.config.unit_system.temperature.indexOf("F")?1:.5}},{key:"supportsTemperatureControls",value:function(e){return this.supportsTemperature(e)}},{key:"supportsTemperature",value:function(e){return(0,c.e)(e,1)&&"number"==typeof e.attributes.temperature}},{key:"supportsOperationMode",value:function(e){return(0,c.e)(e,2)}},{key:"supportsAwayMode",value:function(e){return(0,c.e)(e,4)}},{key:"computeClassNames",value:function(e){var t=[(0,u.d)(e,{1:"has-target_temperature",2:"has-operation_mode",4:"has-away_mode"})];return t.push("more-info-water_heater"),t.join(" ")}},{key:"targetTemperatureChanged",value:function(e){var t=e.target.value;t!==this.stateObj.attributes.temperature&&this.callServiceHelper("set_temperature",{temperature:t})}},{key:"awayToggleChanged",value:function(e){var t="on"===this.stateObj.attributes.away_mode,n=e.target.checked;t!==n&&this.callServiceHelper("set_away_mode",{away_mode:n})}},{key:"handleOperationmodeChanged",value:function(e){var t=this.stateObj.attributes.operation_mode,n=e.detail.value;n&&t!==n&&this.callServiceHelper("set_operation_mode",{operation_mode:n})}},{key:"callServiceHelper",value:function(e,t){var n=this;t.entity_id=this.stateObj.entity_id,this.hass.callService("water_heater",e,t).then((function(){n.stateObjChanged(n.stateObj)}))}},{key:"_localizeOperationMode",value:function(e,t){return e("component.water_heater.state._.".concat(t))||t}}])&&O(t.prototype,n),i&&O(t,i),l}((0,n(1265).Z)((0,s.I)(i.H3)));customElements.define("more-info-water_heater",C)}}]);
//# sourceMappingURL=chunk.27d1d5565122c5e9c3a0.js.map