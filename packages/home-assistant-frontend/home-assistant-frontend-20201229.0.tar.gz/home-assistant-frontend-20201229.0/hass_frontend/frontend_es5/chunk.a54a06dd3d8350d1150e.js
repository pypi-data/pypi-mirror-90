/*! For license information please see chunk.a54a06dd3d8350d1150e.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[9188],{25782:function(e,t,n){"use strict";n(43437),n(65660),n(70019),n(97968);var i=n(9672),r=n(50856),o=n(33760);function a(){var e=function(e,t){t||(t=e.slice(0));return Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(['\n    <style include="paper-item-shared-styles"></style>\n    <style>\n      :host {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n        @apply --paper-font-subhead;\n\n        @apply --paper-item;\n        @apply --paper-icon-item;\n      }\n\n      .content-icon {\n        @apply --layout-horizontal;\n        @apply --layout-center;\n\n        width: var(--paper-item-icon-width, 56px);\n        @apply --paper-item-icon;\n      }\n    </style>\n\n    <div id="contentIcon" class="content-icon">\n      <slot name="item-icon"></slot>\n    </div>\n    <slot></slot>\n']);return a=function(){return e},e}(0,i.k)({_template:(0,r.d)(a()),is:"paper-icon-item",behaviors:[o.U]})},89194:function(e,t,n){"use strict";n(43437),n(65660),n(70019);var i=n(9672),r=n(50856);function o(){var e=function(e,t){t||(t=e.slice(0));return Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(["\n    <style>\n      :host {\n        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */\n        @apply --layout-vertical;\n        @apply --layout-center-justified;\n        @apply --layout-flex;\n      }\n\n      :host([two-line]) {\n        min-height: var(--paper-item-body-two-line-min-height, 72px);\n      }\n\n      :host([three-line]) {\n        min-height: var(--paper-item-body-three-line-min-height, 88px);\n      }\n\n      :host > ::slotted(*) {\n        overflow: hidden;\n        text-overflow: ellipsis;\n        white-space: nowrap;\n      }\n\n      :host > ::slotted([secondary]) {\n        @apply --paper-font-body1;\n\n        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));\n\n        @apply --paper-item-body-secondary;\n      }\n    </style>\n\n    <slot></slot>\n"]);return o=function(){return e},e}(0,i.k)({_template:(0,r.d)(o()),is:"paper-item-body"})},1275:function(e,t,n){"use strict";n.d(t,{l:function(){return o}});var i=n(94707),r=new WeakMap,o=(0,i.XM)((function(e,t){return function(n){var i=r.get(n);if(Array.isArray(e)){if(Array.isArray(i)&&i.length===e.length&&e.every((function(e,t){return e===i[t]})))return}else if(i===e&&(void 0!==e||r.has(n)))return;n.setValue(t()),r.set(n,Array.isArray(e)?Array.from(e):e)}}))},33785:function(e,t,n){"use strict";n.r(t),n.d(t,{HuiPictureGlanceCardEditor:function(){return x}});n(8878),n(30879),n(53973),n(51095);var i=n(15652),r=n(4268),o=n(47181),a=(n(74535),n(26431),n(1528),n(24673),n(14748)),s=n(51598),c=n(45890);function l(e){return(l="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function u(){var e=p([" <paper-item>","</paper-item> "]);return u=function(){return e},e}function f(){var e=p(['\n      <div class="card-config">\n        <paper-input\n          .label="'," (",')"\n          .value="','"\n          .configValue="','"\n          @value-changed="','"\n        ></paper-input>\n        <paper-input\n          .label="'," (",')"\n          .value="','"\n          .configValue="','"\n          @value-changed="','"\n        ></paper-input>\n        <ha-entity-picker\n          .label="'," (",')"\n          .hass=','\n          .value="','"\n          .configValue=','\n          @value-changed="','"\n          allow-custom-entity\n          .includeDomains=','\n        ></ha-entity-picker>\n        <div class="side-by-side">\n          <paper-dropdown-menu\n            .label="'," (",')"\n            .configValue="','"\n            @value-changed="','"\n          >\n            <paper-listbox\n              slot="dropdown-content"\n              .selected="','"\n            >\n              ','\n            </paper-listbox>\n          </paper-dropdown-menu>\n          <paper-input\n            .label="'," (",')"\n            .value="','"\n            .configValue="','"\n            @value-changed="','"\n          ></paper-input>\n        </div>\n        <ha-entity-picker\n          .label="'," (",')"\n          .hass=','\n          .value="','"\n          .configValue=','\n          @value-changed="','"\n          allow-custom-entity\n        ></ha-entity-picker>\n        <div class="side-by-side">\n          <hui-action-editor\n            .label="'," (",')"\n            .hass=','\n            .config="','"\n            .actions="','"\n            .configValue="','"\n            @value-changed="','"\n          ></hui-action-editor>\n          <hui-action-editor\n            .label="'," (",')"\n            .hass=','\n            .config="','"\n            .actions="','"\n            .configValue="','"\n            @value-changed="','"\n          ></hui-action-editor>\n        </div>\n        <hui-entity-editor\n          .hass=','\n          .entities="','"\n          @entities-changed="','"\n        ></hui-entity-editor>\n        <hui-theme-select-editor\n          .hass=','\n          .value="','"\n          .configValue="','"\n          @value-changed="','"\n        ></hui-theme-select-editor>\n      </div>\n    ']);return f=function(){return e},e}function d(){var e=p([""]);return d=function(){return e},e}function p(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function h(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function m(e,t){return(m=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function y(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,i=_(e);if(t){var r=_(this).constructor;n=Reflect.construct(i,arguments,r)}else n=i.apply(this,arguments);return v(this,n)}}function v(e,t){return!t||"object"!==l(t)&&"function"!=typeof t?g(e):t}function g(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function _(e){return(_=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}function b(){b=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var r=t.placement;if(t.kind===i&&("static"===r||"prototype"===r)){var o="static"===r?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var i=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],i=[],r={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,r)}),this),e.forEach((function(e){if(!E(e))return n.push(e);var t=this.decorateElement(e,r);n.push(t.element),n.push.apply(n,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:n,finishers:i};var o=this.decorateConstructor(n,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,n){var i=t[e.placement];if(!n&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var n=[],i=[],r=e.decorators,o=r.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,r[o])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);n.push.apply(n,l)}}return{element:e,finishers:i,extras:n}},decorateConstructor:function(e,t){for(var n=[],i=t.length-1;i>=0;i--){var r=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(r)||r);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return O(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?O(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=C(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var r=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:i,descriptor:Object.assign({},r)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(r,"get","The property descriptor of a field descriptor"),this.disallowProperty(r,"set","The property descriptor of a field descriptor"),this.disallowProperty(r,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:z(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=z(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var i=(0,t[n])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function w(e){var t,n=C(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function k(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function E(e){return e.decorators&&e.decorators.length}function j(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function z(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function C(e){var t=function(e,t){if("object"!==l(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var i=n.call(e,t||"default");if("object"!==l(i))return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===l(t)?t:String(t)}function O(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,i=new Array(t);n<t;n++)i[n]=e[n];return i}var P=(0,r.Ry)({type:(0,r.Z_)(),title:(0,r.jt)((0,r.Z_)()),entity:(0,r.jt)((0,r.Z_)()),image:(0,r.jt)((0,r.Z_)()),camera_image:(0,r.jt)((0,r.Z_)()),camera_view:(0,r.jt)((0,r.Z_)()),aspect_ratio:(0,r.jt)((0,r.Z_)()),tap_action:(0,r.jt)(s.f),hold_action:(0,r.jt)(s.f),entities:(0,r.IX)(s.K),theme:(0,r.jt)((0,r.Z_)())}),A=["camera"],x=function(e,t,n,i){var r=b();if(i)for(var o=0;o<i.length;o++)r=i[o](r);var a=t((function(e){r.initializeInstanceElements(e,s.elements)}),n),s=r.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var r,o=e[i];if("method"===o.kind&&(r=t.find(n)))if(j(o.descriptor)||j(r.descriptor)){if(E(o)||E(r))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");r.descriptor=o.descriptor}else{if(E(o)){if(E(r))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");r.decorators=o.decorators}k(o,r)}else t.push(o)}return t}(a.d.map(w)),e);return r.initializeClassElements(a.F,s.elements),r.runClassFinishers(a.F,s.finishers)}([(0,i.Mo)("hui-picture-glance-card-editor")],(function(e,t){return{F:function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&m(e,t)}(i,t);var n=y(i);function i(){var t;h(this,i);for(var r=arguments.length,o=new Array(r),a=0;a<r;a++)o[a]=arguments[a];return t=n.call.apply(n,[this].concat(o)),e(g(t)),t}return i}(t),d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_configEntities",value:void 0},{kind:"method",key:"setConfig",value:function(e){(0,r.hu)(e,P),this._config=e,this._configEntities=(0,a.Q)(e.entities)}},{kind:"get",key:"_entity",value:function(){return this._config.entity||""}},{kind:"get",key:"_title",value:function(){return this._config.title||""}},{kind:"get",key:"_image",value:function(){return this._config.image||this._camera_image?"":"https://www.home-assistant.io/images/merchandise/shirt-frontpage.png"}},{kind:"get",key:"_camera_image",value:function(){return this._config.camera_image||""}},{kind:"get",key:"_camera_view",value:function(){return this._config.camera_view||"auto"}},{kind:"get",key:"_state_image",value:function(){return this._config.state_image||{}}},{kind:"get",key:"_aspect_ratio",value:function(){return this._config.aspect_ratio||""}},{kind:"get",key:"_tap_action",value:function(){return this._config.tap_action||{action:"toggle"}}},{kind:"get",key:"_hold_action",value:function(){return this._config.hold_action||{action:"more-info"}}},{kind:"get",key:"_theme",value:function(){return this._config.theme||""}},{kind:"method",key:"render",value:function(){if(!this.hass||!this._config)return(0,i.dy)(d());var e=["more-info","toggle","navigate","call-service","none"],t=["auto","live"];return(0,i.dy)(f(),this.hass.localize("ui.panel.lovelace.editor.card.generic.title"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this._title,"title",this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.generic.image"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this._image,"image",this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.generic.camera_image"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this.hass,this._camera_image,"camera_image",this._valueChanged,A,this.hass.localize("ui.panel.lovelace.editor.card.generic.camera_view"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),"camera_view",this._valueChanged,t.indexOf(this._camera_view),t.map((function(e){return(0,i.dy)(u(),e)})),this.hass.localize("ui.panel.lovelace.editor.card.generic.aspect_ratio"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this._aspect_ratio,"aspect_ratio",this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.picture-glance.state_entity"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this.hass,this._entity,"entity",this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.generic.tap_action"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this.hass,this._tap_action,e,"tap_action",this._valueChanged,this.hass.localize("ui.panel.lovelace.editor.card.generic.hold_action"),this.hass.localize("ui.panel.lovelace.editor.card.config.optional"),this.hass,this._hold_action,e,"hold_action",this._valueChanged,this.hass,this._configEntities,this._valueChanged,this.hass,this._theme,"theme",this._valueChanged)}},{kind:"method",key:"_valueChanged",value:function(e){if(this._config&&this.hass){var t=e.target,n=e.detail.value;if(e.detail&&e.detail.entities)this._config=Object.assign({},this._config,{entities:e.detail.entities}),this._configEntities=(0,a.Q)(this._config.entities);else if(t.configValue){if(this["_".concat(t.configValue)]===n)return;!1===n||n?this._config=Object.assign({},this._config,function(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}({},t.configValue,n)):(this._config=Object.assign({},this._config),delete this._config[t.configValue])}(0,o.B)(this,"config-changed",{config:this._config})}}},{kind:"get",static:!0,key:"styles",value:function(){return c.A}}]}}),i.oi)},14748:function(e,t,n){"use strict";function i(e){return e.map((function(e){return"string"==typeof e?{entity:e}:e}))}n.d(t,{Q:function(){return i}})}}]);
//# sourceMappingURL=chunk.a54a06dd3d8350d1150e.js.map