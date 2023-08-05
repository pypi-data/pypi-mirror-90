(()=>{"use strict";const e=Symbol("Comlink.proxy"),t=Symbol("Comlink.endpoint"),n=Symbol("Comlink.releaseProxy"),r=Symbol("Comlink.thrown"),a=e=>"object"==typeof e&&null!==e||"function"==typeof e,s=new Map([["proxy",{canHandle:t=>a(t)&&t[e],serialize(e){const{port1:t,port2:n}=new MessageChannel;return o(e,t),[n,[n]]},deserialize(e){return e.start(),l(e,[],t);var t}}],["throw",{canHandle:e=>a(e)&&r in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function o(t,n=self){n.addEventListener("message",(function a(s){if(!s||!s.data)return;const{id:c,type:l,path:u}=Object.assign({path:[]},s.data),d=(s.data.argumentList||[]).map(m);let y;try{const n=u.slice(0,-1).reduce(((e,t)=>e[t]),t),r=u.reduce(((e,t)=>e[t]),t);switch(l){case 0:y=r;break;case 1:n[u.slice(-1)[0]]=m(s.data.value),y=!0;break;case 2:y=r.apply(n,d);break;case 3:y=function(t){return Object.assign(t,{[e]:!0})}(new r(...d));break;case 4:{const{port1:e,port2:n}=new MessageChannel;o(t,n),y=function(e,t){return p.set(e,t),e}(e,[e])}break;case 5:y=void 0}}catch(e){y={value:e,[r]:0}}Promise.resolve(y).catch((e=>({value:e,[r]:0}))).then((e=>{const[t,r]=f(e);n.postMessage(Object.assign(Object.assign({},t),{id:c}),r),5===l&&(n.removeEventListener("message",a),i(n))}))})),n.start&&n.start()}function i(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function c(e){if(e)throw new Error("Proxy has been released and is not useable")}function l(e,r=[],a=function(){}){let s=!1;const o=new Proxy(a,{get(t,a){if(c(s),a===n)return()=>d(e,{type:5,path:r.map((e=>e.toString()))}).then((()=>{i(e),s=!0}));if("then"===a){if(0===r.length)return{then:()=>o};const t=d(e,{type:0,path:r.map((e=>e.toString()))}).then(m);return t.then.bind(t)}return l(e,[...r,a])},set(t,n,a){c(s);const[o,i]=f(a);return d(e,{type:1,path:[...r,n].map((e=>e.toString())),value:o},i).then(m)},apply(n,a,o){c(s);const i=r[r.length-1];if(i===t)return d(e,{type:4}).then(m);if("bind"===i)return l(e,r.slice(0,-1));const[p,f]=u(o);return d(e,{type:2,path:r.map((e=>e.toString())),argumentList:p},f).then(m)},construct(t,n){c(s);const[a,o]=u(n);return d(e,{type:3,path:r.map((e=>e.toString())),argumentList:a},o).then(m)}});return o}function u(e){const t=e.map(f);return[t.map((e=>e[0])),(n=t.map((e=>e[1])),Array.prototype.concat.apply([],n))];var n}const p=new WeakMap;function f(e){for(const[t,n]of s)if(n.canHandle(e)){const[r,a]=n.serialize(e);return[{type:3,name:t,value:r},a]}return[{type:0,value:e},p.get(e)||[]]}function m(e){switch(e.type){case 3:return s.get(e.name).deserialize(e.value);case 0:return e.value}}function d(e,t,n){return new Promise((r=>{const a=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");e.addEventListener("message",(function t(n){n.data&&n.data.id&&n.data.id===a&&(e.removeEventListener("message",t),r(n.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:a},t),n)}))}o({filterData:(e,t,n)=>(n=n.toUpperCase(),e.filter((e=>Object.entries(t).some((t=>{const[r,a]=t;return!(!a.filterable||!String(a.filterKey?e[r][a.filterKey]:e[r]).toUpperCase().includes(n))}))))),sortData:(e,t,n,r)=>e.sort(((e,a)=>{let s=1;"desc"===n&&(s=-1);let o=t.filterKey?e[r][t.filterKey]:e[r],i=t.filterKey?a[r][t.filterKey]:a[r];return"string"==typeof o&&(o=o.toUpperCase()),"string"==typeof i&&(i=i.toUpperCase()),void 0===o&&void 0!==i?1:void 0===i&&void 0!==o?-1:o<i?-1*s:o>i?1*s:0}))})})();
//# sourceMappingURL=chunk.3515b1ffe9313f6c3acf.js.map