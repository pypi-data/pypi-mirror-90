(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[3775],{93888:function(e,t,n){"use strict";n.r(t);n(81689);var r=n(55317),i=n(15652),o=n(81471),s=n(14516),a=n(47181),c=n(58831),l=n(91741),u=n(45485),d=n(85415),f=n(87744),p=(n(65992),n(81545),n(22098),n(83927),n(10983),n(43709),n(83270)),h=n(90363),m=(n(15291),n(60010),n(11654)),y=n(81796);function v(e){return(v="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function g(){var e=j(['\n        mwc-list-item > [slot="meta"] {\n          margin-left: 4px;\n        }\n        .banner {\n          color: var(--primary-text-color);\n          background-color: var(\n            --ha-card-background,\n            var(--card-background-color, white)\n          );\n          padding: 16px 8px;\n          text-align: center;\n        }\n        .content {\n          display: grid;\n          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));\n          grid-gap: 8px 8px;\n          padding: 8px;\n        }\n        .card-content {\n          padding-bottom: 12px;\n        }\n        state-info {\n          cursor: pointer;\n        }\n        ha-switch {\n          padding: 8px 0;\n        }\n        .top-line {\n          display: flex;\n          align-items: center;\n          justify-content: space-between;\n        }\n        .header {\n          display: flex;\n          align-items: center;\n          justify-content: space-between;\n          padding: 0 16px;\n          border-bottom: 1px solid var(--divider-color);\n          background: var(--app-header-background-color);\n        }\n        .header.second {\n          border-top: 1px solid var(--divider-color);\n        }\n        .exposed {\n          color: var(--success-color);\n        }\n        .not-exposed {\n          color: var(--error-color);\n        }\n        @media all and (max-width: 450px) {\n          ha-card {\n            max-width: 100%;\n          }\n        }\n      ']);return g=function(){return e},e}function b(e,t,n,r,i,o,s){try{var a=e[o](s),c=a.value}catch(l){return void n(l)}a.done?t(c):Promise.resolve(c).then(r,i)}function _(e){return function(){var t=this,n=arguments;return new Promise((function(r,i){var o=e.apply(t,n);function s(e){b(o,r,i,s,a,"next",e)}function a(e){b(o,r,i,s,a,"throw",e)}s(void 0)}))}}function k(){var e=j(['\n                  <div class="header second">\n                    <h3>\n                      ',"\n                    </h3>\n                    ",'\n                  </div>\n                  <div class="content">',"</div>\n                "]);return k=function(){return e},e}function w(){var e=j(['\n                  <div class="header">\n                    <h3>\n                      ',"\n                    </h3>\n                    ",'\n                  </div>\n                  <div class="content">',"</div>\n                "]);return w=function(){return e},e}function x(){var e=j(['\n                <div class="banner">\n                  ',"\n                </div>\n              "]);return x=function(){return e},e}function E(){var e=j(['\n                <mwc-button\n                  slot="toolbar-icon"\n                  @click=',"\n                  >","</mwc-button\n                >\n              "]);return E=function(){return e},e}function S(){var e=j(["\n      <hass-subpage \n        .hass=","\n        .header=",">\n        ","\n        ","\n          ","\n          ","\n        </div>\n      </hass-subpage>\n    "]);return S=function(){return e},e}function C(){var e=j(["\n                  <div>\n                    <ha-formfield\n                      .label=","\n                      .dir=","\n                    >\n                      <ha-switch\n                        .entityId=","\n                        .checked=","\n                        @change=","\n                      ></ha-switch>\n                    </ha-formfield>\n                  </div>\n                "]);return C=function(){return e},e}function D(){var e=j(['<ha-button-menu\n                    corner="BOTTOM_START"\n                    .entityId=',"\n                    @action=","\n                  >\n                    ","\n                    <mwc-list-item hasMeta>\n                      ",'\n                      <ha-svg-icon\n                        class="exposed"\n                        slot="meta"\n                        .path=',"\n                      ></ha-svg-icon>\n                    </mwc-list-item>\n                    <mwc-list-item hasMeta>\n                      ",'\n                      <ha-svg-icon\n                        class="not-exposed"\n                        slot="meta"\n                        .path=',"\n                      ></ha-svg-icon>\n                    </mwc-list-item>\n                    <mwc-list-item hasMeta>\n                      ","\n                      <ha-svg-icon\n                        class=",'\n                        slot="meta"\n                        .path=',"\n                      ></ha-svg-icon>\n                    </mwc-list-item>\n                  </ha-button-menu>"]);return D=function(){return e},e}function O(){var e=j(["",""]);return O=function(){return e},e}function P(){var e=j(['\n        <ha-card>\n          <div class="card-content">\n            <div class="top-line">\n              <state-info\n                .hass=',"\n                .stateObj=","\n                secondary-line\n                @click=","\n              >\n                ","\n              </state-info>\n              ","\n            </div>\n            ","\n          </div>\n        </ha-card>\n      "]);return P=function(){return e},e}function A(){var e=j(['<mwc-icon-button\n        slot="trigger"\n        class=',"\n        .disabled=","\n        .title=","\n      >\n        <ha-svg-icon\n          .path=","\n        ></ha-svg-icon>\n      </mwc-icon-button>"]);return A=function(){return e},e}function R(){var e=j([" <hass-loading-screen></hass-loading-screen> "]);return R=function(){return e},e}function j(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}function z(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function T(e,t){return(T=Object.setPrototypeOf||function(e,t){return e.__proto__=t,e})(e,t)}function I(e){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(e){return!1}}();return function(){var n,r=V(e);if(t){var i=V(this).constructor;n=Reflect.construct(r,arguments,i)}else n=r.apply(this,arguments);return F(this,n)}}function F(e,t){return!t||"object"!==v(t)&&"function"!=typeof t?M(e):t}function M(e){if(void 0===e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return e}function B(){B=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(n){t.forEach((function(t){t.kind===n&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var n=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var i=t.placement;if(t.kind===r&&("static"===i||"prototype"===i)){var o="static"===i?e:n;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var n=t.descriptor;if("field"===t.kind){var r=t.initializer;n={enumerable:n.enumerable,writable:n.writable,configurable:n.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,n)},decorateClass:function(e,t){var n=[],r=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!L(e))return n.push(e);var t=this.decorateElement(e,i);n.push(t.element),n.push.apply(n,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:n,finishers:r};var o=this.decorateConstructor(n,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,n){var r=t[e.placement];if(!n&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var n=[],r=[],i=e.decorators,o=i.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,i[o])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var u=0;u<l.length;u++)this.addElementPlacement(l[u],t);n.push.apply(n,l)}}return{element:e,finishers:r,extras:n}},decorateConstructor:function(e,t){for(var n=[],r=t.length-1;r>=0;r--){var i=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(i)||i);if(void 0!==o.finisher&&n.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:n}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return Q(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?Q(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var n=H(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:n,placement:r,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:U(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var n=U(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:n}},runClassFinishers:function(e,t){for(var n=0;n<t.length;n++){var r=(0,t[n])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,n){if(void 0!==e[t])throw new TypeError(n+" can't have a ."+t+" property.")}};return e}function $(e){var t,n=H(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:n,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function q(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function L(e){return e.decorators&&e.decorators.length}function N(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function U(e,t){var n=e[t];if(void 0!==n&&"function"!=typeof n)throw new TypeError("Expected '"+t+"' to be a function");return n}function H(e){var t=function(e,t){if("object"!==v(e)||null===e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,t||"default");if("object"!==v(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"===v(t)?t:String(t)}function Q(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function Z(e,t,n){return(Z="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,n){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=V(e)););return e}(e,t);if(r){var i=Object.getOwnPropertyDescriptor(r,t);return i.get?i.get.call(n):i.value}})(e,t,n||e)}function V(e){return(V=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,n,r){var i=B();if(r)for(var o=0;o<r.length;o++)i=r[o](i);var s=t((function(e){i.initializeInstanceElements(e,a.elements)}),n),a=i.decorateClass(function(e){for(var t=[],n=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var i,o=e[r];if("method"===o.kind&&(i=t.find(n)))if(N(o.descriptor)||N(i.descriptor)){if(L(o)||L(i))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");i.descriptor=o.descriptor}else{if(L(o)){if(L(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");i.decorators=o.decorators}q(o,i)}else t.push(o)}return t}(s.d.map($)),e);i.initializeClassElements(s.F,a.elements),i.runClassFinishers(s.F,a.finishers)}([(0,i.Mo)("cloud-google-assistant")],(function(e,t){var n,v,b,j,F,B,$=function(t){!function(e,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,writable:!0,configurable:!0}}),t&&T(e,t)}(r,t);var n=I(r);function r(){var t;z(this,r);for(var i=arguments.length,o=new Array(i),s=0;s<i;s++)o[s]=arguments[s];return t=n.call.apply(n,[this].concat(o)),e(M(t)),t}return r}(t);return{F:$,d:[{kind:"field",decorators:[(0,i.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"cloudStatus",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,i.sz)()],key:"_entities",value:void 0},{kind:"field",decorators:[(0,i.Cb)()],key:"_entityConfigs",value:function(){return{}}},{kind:"field",key:"_popstateSyncAttached",value:function(){return!1}},{kind:"field",key:"_popstateReloadStatusAttached",value:function(){return!1}},{kind:"field",key:"_isInitialExposed",value:void 0},{kind:"field",key:"_getEntityFilterFunc",value:function(){return(0,s.Z)((function(e){return(0,u.h)(e.include_domains,e.include_entities,e.exclude_domains,e.exclude_entities)}))}},{kind:"method",key:"render",value:function(){var e=this;if(void 0===this._entities)return(0,i.dy)(R());var t=(0,u.E)(this.cloudStatus.google_entities),n=this._getEntityFilterFunc(this.cloudStatus.google_entities),s=(0,f.Zu)(this.hass),a=this._isInitialExposed||new Set,c=void 0===this._isInitialExposed,l=0,d=[],p=[];return this._entities.forEach((function(u){var f=e.hass.states[u.entity_id],h=e._entityConfigs[u.entity_id]||{should_expose:null},m=t?e._configIsExposed(u.entity_id,h):n(u.entity_id),y=t?e._configIsDomainExposed(u.entity_id):n(u.entity_id);m&&(l++,c&&a.add(u.entity_id));var v=a.has(u.entity_id)?d:p,g=(0,i.dy)(A(),(0,o.$)({exposed:m,"not-exposed":!m}),!t,e.hass.localize("ui.panel.config.cloud.google.expose"),null!==h.should_expose?m?r.qtl:r.xaH:y?r.D4N:r.tyg);v.push((0,i.dy)(P(),e.hass,f,e._showMoreInfo,u.traits.map((function(e){return e.substr(e.lastIndexOf(".")+1)})).join(", "),t?(0,i.dy)(D(),f.entity_id,e._exposeChanged,g,e.hass.localize("ui.panel.config.cloud.google.expose_entity"),r.qtl,e.hass.localize("ui.panel.config.cloud.google.dont_expose_entity"),r.xaH,e.hass.localize("ui.panel.config.cloud.google.follow_domain"),(0,o.$)({exposed:y,"not-exposed":!y}),y?r.D4N:r.tyg):(0,i.dy)(O(),g),u.might_2fa?(0,i.dy)(C(),e.hass.localize("ui.panel.config.cloud.google.disable_2FA"),s,u.entity_id,Boolean(h.disable_2fa),e._disable2FAChanged):""))})),c&&(this._isInitialExposed=a),(0,i.dy)(S(),this.hass,this.hass.localize("ui.panel.config.cloud.google.title"),t?(0,i.dy)(E(),this._openDomainToggler,this.hass.localize("ui.panel.config.cloud.google.manage_domains")):"",t?"":(0,i.dy)(x(),this.hass.localize("ui.panel.config.cloud.google.banner")),d.length>0?(0,i.dy)(w(),this.hass.localize("ui.panel.config.cloud.google.exposed_entities"),this.narrow?l:this.hass.localize("ui.panel.config.cloud.alexa.exposed","selected",l),d):"",p.length>0?(0,i.dy)(k(),this.hass.localize("ui.panel.config.cloud.google.not_exposed_entities"),this.narrow?this._entities.length-l:this.hass.localize("ui.panel.config.cloud.alexa.not_exposed","selected",this._entities.length-l),p):"")}},{kind:"method",key:"firstUpdated",value:function(e){Z(V($.prototype),"firstUpdated",this).call(this,e),this._fetchData()}},{kind:"method",key:"updated",value:function(e){Z(V($.prototype),"updated",this).call(this,e),e.has("cloudStatus")&&(this._entityConfigs=this.cloudStatus.prefs.google_entity_configs)}},{kind:"method",key:"_configIsDomainExposed",value:function(e){var t=(0,c.M)(e);return!this.cloudStatus.prefs.google_default_expose||this.cloudStatus.prefs.google_default_expose.includes(t)}},{kind:"method",key:"_configIsExposed",value:function(e,t){var n;return null!==(n=t.should_expose)&&void 0!==n?n:this._configIsDomainExposed(e)}},{kind:"method",key:"_fetchData",value:(B=_(regeneratorRuntime.mark((function e(){var t,n=this;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this.hass.callWS({type:"cloud/google_assistant/entities"});case 2:(t=e.sent).sort((function(e,t){var r=n.hass.states[e.entity_id],i=n.hass.states[t.entity_id];return(0,d.q)(r?(0,l.C)(r):e.entity_id,i?(0,l.C)(i):t.entity_id)})),this._entities=t;case 5:case"end":return e.stop()}}),e,this)}))),function(){return B.apply(this,arguments)})},{kind:"method",key:"_showMoreInfo",value:function(e){var t=e.currentTarget.stateObj.entity_id;(0,a.B)(this,"hass-more-info",{entityId:t})}},{kind:"method",key:"_exposeChanged",value:(F=_(regeneratorRuntime.mark((function e(t){var n,r;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:n=t.currentTarget.entityId,r=null,e.t0=t.detail.index,e.next=0===e.t0?5:1===e.t0?7:2===e.t0?9:11;break;case 5:return r=!0,e.abrupt("break",11);case 7:return r=!1,e.abrupt("break",11);case 9:return r=null,e.abrupt("break",11);case 11:return e.next=13,this._updateExposed(n,r);case 13:case"end":return e.stop()}}),e,this)}))),function(e){return F.apply(this,arguments)})},{kind:"method",key:"_updateExposed",value:(j=_(regeneratorRuntime.mark((function e(t,n){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,this._updateConfig(t,{should_expose:n});case 2:this._ensureEntitySync();case 3:case"end":return e.stop()}}),e,this)}))),function(e,t){return j.apply(this,arguments)})},{kind:"method",key:"_disable2FAChanged",value:(b=_(regeneratorRuntime.mark((function e(t){var n,r,i;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(n=t.currentTarget.entityId,r=t.target.checked,i=Boolean((this._entityConfigs[n]||{}).disable_2fa),r!==i){e.next=5;break}return e.abrupt("return");case 5:return e.next=7,this._updateConfig(n,{disable_2fa:r});case 7:case"end":return e.stop()}}),e,this)}))),function(e){return b.apply(this,arguments)})},{kind:"method",key:"_updateConfig",value:(v=_(regeneratorRuntime.mark((function e(t,n){var r;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,(0,p.QD)(this.hass,t,n);case 2:r=e.sent,this._entityConfigs=Object.assign({},this._entityConfigs,(s=r,(o=t)in(i={})?Object.defineProperty(i,o,{value:s,enumerable:!0,configurable:!0,writable:!0}):i[o]=s,i)),this._ensureStatusReload();case 5:case"end":return e.stop()}var i,o,s}),e,this)}))),function(e,t){return v.apply(this,arguments)})},{kind:"method",key:"_openDomainToggler",value:function(){var e=this;(0,h._)(this,{domains:this._entities.map((function(e){return(0,c.M)(e.entity_id)})).filter((function(e,t,n){return n.indexOf(e)===t})),exposedDomains:this.cloudStatus.prefs.google_default_expose,toggleDomain:function(t,n){e._updateDomainExposed(t,n)},resetDomain:function(t){e._entities.forEach((function(n){(0,c.M)(n.entity_id)===t&&e._updateExposed(n.entity_id,null)}))}})}},{kind:"method",key:"_updateDomainExposed",value:(n=_(regeneratorRuntime.mark((function e(t,n){var r;return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(r=this.cloudStatus.prefs.google_default_expose||this._entities.map((function(e){return(0,c.M)(e.entity_id)})).filter((function(e,t,n){return n.indexOf(e)===t})),!(n&&r.includes(t)||!n&&!r.includes(t))){e.next=3;break}return e.abrupt("return");case 3:return n?r.push(t):r.splice(r.indexOf(t),1),e.next=6,(0,p.LV)(this.hass,{google_default_expose:r});case 6:(0,a.B)(this,"ha-refresh-cloud-status");case 7:case"end":return e.stop()}}),e,this)}))),function(e,t){return n.apply(this,arguments)})},{kind:"method",key:"_ensureStatusReload",value:function(){if(!this._popstateReloadStatusAttached){this._popstateReloadStatusAttached=!0;var e=this.parentElement;window.addEventListener("popstate",(function(){return(0,a.B)(e,"ha-refresh-cloud-status")}),{once:!0})}}},{kind:"method",key:"_ensureEntitySync",value:function(){var e=this;if(!this._popstateSyncAttached){this._popstateSyncAttached=!0;var t=this.parentElement;window.addEventListener("popstate",(function(){(0,y.C)(t,{message:e.hass.localize("ui.panel.config.cloud.google.sync_to_google")}),(0,p.A$)(e.hass)}),{once:!0})}}},{kind:"get",static:!0,key:"styles",value:function(){return[m.Qx,(0,i.iv)(g())]}}]}}),i.oi)}}]);
//# sourceMappingURL=chunk.93879e72666b6e7cd8b6.js.map