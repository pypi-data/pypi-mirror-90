/*! For license information please see chunk.fdbbf3d8450b3cd67f9f.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[2179,808],{79332:function(n,t,e){"use strict";e.d(t,{a:function(){return i}});e(43437);var i={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(n,t){for(var e in t)n[e]=t[e]},_cloneConfig:function(n){var t={isClone:!0};return this._copyProperties(t,n),t},_getAnimationConfigRecursive:function(n,t,e){var i;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(i=n?this.animationConfig[n]:this.animationConfig,Array.isArray(i)||(i=[i]),i)for(var o,a=0;o=i[a];a++)if(o.animatable)o.animatable._getAnimationConfigRecursive(o.type||n,t,e);else if(o.id){var r=t[o.id];r?(r.isClone||(t[o.id]=this._cloneConfig(r),r=t[o.id]),this._copyProperties(r,o)):t[o.id]=o}else e.push(o)},getAnimationConfig:function(n){var t={},e=[];for(var i in this._getAnimationConfigRecursive(n,t,e),t)e.push(t[i]);return e}}},96540:function(n,t,e){"use strict";e.d(t,{t:function(){return o}});e(43437);var i={_configureAnimations:function(n){var t=[],e=[];if(n.length>0)for(var i,o=0;i=n[o];o++){var a=document.createElement(i.name);if(a.isNeonAnimation){var r;a.configure||(a.configure=function(n){return null}),r=a.configure(i),e.push({result:r,config:i,neonAnimation:a})}else console.warn(this.is+":",i.name,"not found!")}for(var s=0;s<e.length;s++){var l=e[s].result,c=e[s].config,u=e[s].neonAnimation;try{"function"!=typeof l.cancel&&(l=document.timeline.play(l))}catch(p){l=null,console.warn("Couldnt play","(",c.name,").",p)}l&&t.push({neonAnimation:u,config:c,animation:l})}return t},_shouldComplete:function(n){for(var t=!0,e=0;e<n.length;e++)if("finished"!=n[e].animation.playState){t=!1;break}return t},_complete:function(n){for(var t=0;t<n.length;t++)n[t].neonAnimation.complete(n[t].config);for(t=0;t<n.length;t++)n[t].animation.cancel()},playAnimation:function(n,t){var e=this.getAnimationConfig(n);if(e){this._active=this._active||{},this._active[n]&&(this._complete(this._active[n]),delete this._active[n]);var i=this._configureAnimations(e);if(0!=i.length){this._active[n]=i;for(var o=0;o<i.length;o++)i[o].animation.onfinish=function(){this._shouldComplete(i)&&(this._complete(i),delete this._active[n],this.fire("neon-animation-finish",t,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",t,{bubbles:!1})}},cancelAnimation:function(){for(var n in this._active){var t=this._active[n];for(var e in t)t[e].animation.cancel()}this._active={}}},o=[e(79332).a,i]},51654:function(n,t,e){"use strict";e.d(t,{Z:function(){return a},n:function(){return r}});e(43437);var i=e(75009),o=e(87156),a={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(n,t){t&&(n?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(n){this.closingReason=this.closingReason||{},this.closingReason.confirmed=n},_onDialogClick:function(n){for(var t=(0,o.vz)(n).path,e=0,i=t.indexOf(this);e<i;e++){var a=t[e];if(a.hasAttribute&&(a.hasAttribute("dialog-dismiss")||a.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(a.hasAttribute("dialog-confirm")),this.close(),n.stopPropagation();break}}}},r=[i.$,a]},50808:function(n,t,e){"use strict";e(43437),e(65660),e(70019),e(54242);var i=document.createElement("template");i.setAttribute("style","display: none;"),i.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(i.content);var o=e(96540),a=e(51654),r=e(9672),s=e(50856);function l(){var n=function(n,t){t||(t=n.slice(0));return Object.freeze(Object.defineProperties(n,{raw:{value:Object.freeze(t)}}))}(['\n    <style include="paper-dialog-shared-styles"></style>\n    <slot></slot>\n']);return l=function(){return n},n}(0,r.k)({_template:(0,s.d)(l()),is:"paper-dialog",behaviors:[a.n,o.t],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},28417:function(n,t,e){"use strict";e(50808);var i=e(33367),o=e(93592),a=e(87156),r={getTabbableNodes:function(n){var t=[];return this._collectTabbableNodes(n,t)?o.H._sortByTabIndex(t):t},_collectTabbableNodes:function(n,t){if(n.nodeType!==Node.ELEMENT_NODE||!o.H._isVisible(n))return!1;var e,i=n,r=o.H._normalizedTabIndex(i),s=r>0;r>=0&&t.push(i),e="content"===i.localName||"slot"===i.localName?(0,a.vz)(i).getDistributedNodes():(0,a.vz)(i.shadowRoot||i.root||i).children;for(var l=0;l<e.length;l++)s=this._collectTabbableNodes(e[l],t)||s;return s}};function s(n){return(s="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(n){return typeof n}:function(n){return n&&"function"==typeof Symbol&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n})(n)}function l(n,t){if(!(n instanceof t))throw new TypeError("Cannot call a class as a function")}function c(n,t){return(c=Object.setPrototypeOf||function(n,t){return n.__proto__=t,n})(n,t)}function u(n){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(n){return!1}}();return function(){var e,i=f(n);if(t){var o=f(this).constructor;e=Reflect.construct(i,arguments,o)}else e=i.apply(this,arguments);return p(this,e)}}function p(n,t){return!t||"object"!==s(t)&&"function"!=typeof t?function(n){if(void 0===n)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return n}(n):t}function f(n){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(n){return n.__proto__||Object.getPrototypeOf(n)})(n)}var d=customElements.get("paper-dialog"),h={get _focusableNodes(){return r.getTabbableNodes(this)}},m=function(n){!function(n,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");n.prototype=Object.create(t&&t.prototype,{constructor:{value:n,writable:!0,configurable:!0}}),t&&c(n,t)}(e,n);var t=u(e);function e(){return l(this,e),t.apply(this,arguments)}return e}((0,i.P)([h],d));customElements.define("ha-paper-dialog",m)},22179:function(n,t,e){"use strict";e.r(t);e(53918),e(31206);var i=e(50856),o=e(28426),a=(e(28417),e(1265));e(36436);function r(n){return(r="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(n){return typeof n}:function(n){return n&&"function"==typeof Symbol&&n.constructor===Symbol&&n!==Symbol.prototype?"symbol":typeof n})(n)}function s(){var n=function(n,t){t||(t=n.slice(0));return Object.freeze(Object.defineProperties(n,{raw:{value:Object.freeze(t)}}))}(['\n      <style include="ha-style-dialog">\n        .error {\n          color: red;\n        }\n        @media all and (max-width: 500px) {\n          ha-paper-dialog {\n            margin: 0;\n            width: 100%;\n            max-height: calc(100% - var(--header-height));\n\n            position: fixed !important;\n            bottom: 0px;\n            left: 0px;\n            right: 0px;\n            overflow: scroll;\n            border-bottom-left-radius: 0px;\n            border-bottom-right-radius: 0px;\n          }\n        }\n\n        ha-paper-dialog {\n          border-radius: 2px;\n        }\n        ha-paper-dialog p {\n          color: var(--secondary-text-color);\n        }\n\n        .icon {\n          float: right;\n        }\n      </style>\n      <ha-paper-dialog\n        id="mp3dialog"\n        with-backdrop\n        opened="{{_opened}}"\n        on-opened-changed="_openedChanged"\n      >\n        <h2>\n          [[localize(\'ui.panel.mailbox.playback_title\')]]\n          <div class="icon">\n            <template is="dom-if" if="[[_loading]]">\n              <ha-circular-progress active></ha-circular-progress>\n            </template>\n            <ha-icon-button\n              id="delicon"\n              on-click="openDeleteDialog"\n              icon="hass:delete"\n            ></ha-icon-button>\n          </div>\n        </h2>\n        <div id="transcribe"></div>\n        <div>\n          <template is="dom-if" if="[[_errorMsg]]">\n            <div class="error">[[_errorMsg]]</div>\n          </template>\n          <audio id="mp3" preload="none" controls>\n            <source id="mp3src" src="" type="audio/mpeg" />\n          </audio>\n        </div>\n      </ha-paper-dialog>\n    ']);return s=function(){return n},n}function l(n,t){if(!(n instanceof t))throw new TypeError("Cannot call a class as a function")}function c(n,t){for(var e=0;e<t.length;e++){var i=t[e];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(n,i.key,i)}}function u(n,t){return(u=Object.setPrototypeOf||function(n,t){return n.__proto__=t,n})(n,t)}function p(n){var t=function(){if("undefined"==typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"==typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(n){return!1}}();return function(){var e,i=d(n);if(t){var o=d(this).constructor;e=Reflect.construct(i,arguments,o)}else e=i.apply(this,arguments);return f(this,e)}}function f(n,t){return!t||"object"!==r(t)&&"function"!=typeof t?function(n){if(void 0===n)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return n}(n):t}function d(n){return(d=Object.setPrototypeOf?Object.getPrototypeOf:function(n){return n.__proto__||Object.getPrototypeOf(n)})(n)}var h=function(n){!function(n,t){if("function"!=typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function");n.prototype=Object.create(t&&t.prototype,{constructor:{value:n,writable:!0,configurable:!0}}),t&&u(n,t)}(r,n);var t,e,o,a=p(r);function r(){return l(this,r),a.apply(this,arguments)}return t=r,o=[{key:"template",get:function(){return(0,i.d)(s())}},{key:"properties",get:function(){return{hass:Object,_currentMessage:Object,_errorMsg:String,_loading:{type:Boolean,value:!1},_opened:{type:Boolean,value:!1}}}}],(e=[{key:"showDialog",value:function(n){var t=this,e=n.hass,i=n.message;this.hass=e,this._errorMsg=null,this._currentMessage=i,this._opened=!0,this.$.transcribe.innerText=i.message;var o=i.platform,a=this.$.mp3;if(o.has_media){a.style.display="",this._showLoading(!0),a.src=null;var r="/api/mailbox/media/".concat(o.name,"/").concat(i.sha);this.hass.fetchWithAuth(r).then((function(n){return n.ok?n.blob():Promise.reject({status:n.status,statusText:n.statusText})})).then((function(n){t._showLoading(!1),a.src=window.URL.createObjectURL(n),a.play()})).catch((function(n){t._showLoading(!1),t._errorMsg="Error loading audio: ".concat(n.statusText)}))}else a.style.display="none",this._showLoading(!1)}},{key:"openDeleteDialog",value:function(){confirm(this.localize("ui.panel.mailbox.delete_prompt"))&&this.deleteSelected()}},{key:"deleteSelected",value:function(){var n=this._currentMessage;this.hass.callApi("DELETE","mailbox/delete/".concat(n.platform.name,"/").concat(n.sha)),this._dialogDone()}},{key:"_dialogDone",value:function(){this.$.mp3.pause(),this.setProperties({_currentMessage:null,_errorMsg:null,_loading:!1,_opened:!1})}},{key:"_openedChanged",value:function(n){n.detail.value||this._dialogDone()}},{key:"_showLoading",value:function(n){var t=this.$.delicon;if(n)this._loading=!0,t.style.display="none";else{var e=this._currentMessage.platform;this._loading=!1,t.style.display=e.can_delete?"":"none"}}}])&&c(t.prototype,e),o&&c(t,o),r}((0,a.Z)(o.H3));customElements.define("ha-dialog-show-audio-message",h)},36436:function(n,t,e){"use strict";e(21384);var i=e(11654),o=document.createElement("template");o.setAttribute("style","display: none;"),o.innerHTML='<dom-module id="ha-style-dialog">\n<template>\n  <style>\n    '.concat(i.yu.cssText,"\n  </style>\n</template>\n</dom-module>"),document.head.appendChild(o.content)}}]);
//# sourceMappingURL=chunk.fdbbf3d8450b3cd67f9f.js.map