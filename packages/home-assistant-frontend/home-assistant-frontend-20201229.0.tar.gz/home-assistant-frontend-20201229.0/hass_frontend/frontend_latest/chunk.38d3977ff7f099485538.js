(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[1480],{81480:(t,e,s)=>{"use strict";function n(t){return Array.isArray?Array.isArray(t):"[object Array]"===Object.prototype.toString.call(t)}s.d(e,{Z:()=>q});function r(t){return"string"==typeof t}function i(t){return"number"==typeof t}function c(t){return null!=t}function h(t){return!t.trim().length}const o=Object.prototype.hasOwnProperty;class a{constructor(t){this._keys={},this._keyNames=[];let e=0;t.forEach((t=>{let s,n=1;if(r(t))s=t;else{if(!o.call(t,"name"))throw new Error(`Missing ${"name"} property in key`);if(s=t.name,o.call(t,"weight")&&(n=t.weight,n<=0))throw new Error((t=>`Property 'weight' in key '${t}' must be a positive integer`)(s))}this._keyNames.push(s),this._keys[s]={weight:n},e+=n})),this._keyNames.forEach((t=>{this._keys[t].weight/=e}))}get(t,e){return this._keys[t]&&this._keys[t][e]}keys(){return this._keyNames}toJSON(){return JSON.stringify(this._keys)}}var l={isCaseSensitive:!1,includeScore:!1,keys:[],shouldSort:!0,sortFn:(t,e)=>t.score===e.score?t.idx<e.idx?-1:1:t.score<e.score?-1:1,includeMatches:!1,findAllMatches:!1,minMatchCharLength:1,location:0,threshold:.6,distance:100,...{useExtendedSearch:!1,getFn:function(t,e){let s=[],h=!1;const o=(t,e)=>{if(e){const a=e.indexOf(".");let l=e,u=null;-1!==a&&(l=e.slice(0,a),u=e.slice(a+1));const d=t[l];if(!c(d))return;if(u||!r(d)&&!i(d))if(n(d)){h=!0;for(let t=0,e=d.length;t<e;t+=1)o(d[t],u)}else u&&o(d,u);else s.push(function(t){return null==t?"":function(t){if("string"==typeof t)return t;let e=t+"";return"0"==e&&1/t==-1/0?"-0":e}(t)}(d))}else s.push(t)};return o(t,e),h?s:s[0]}}};const u=/[^ ]+/g;class d{constructor({getFn:t=l.getFn}={}){this.norm=function(t=3){const e=new Map;return{get(s){const n=s.match(u).length;if(e.has(n))return e.get(n);const r=parseFloat((1/Math.sqrt(n)).toFixed(t));return e.set(n,r),r},clear(){e.clear()}}}(3),this.getFn=t,this.isCreated=!1,this.setRecords()}setCollection(t=[]){this.docs=t}setRecords(t=[]){this.records=t}setKeys(t=[]){this.keys=t}create(){!this.isCreated&&this.docs.length&&(this.isCreated=!0,r(this.docs[0])?this.docs.forEach(((t,e)=>{this._addString(t,e)})):this.docs.forEach(((t,e)=>{this._addObject(t,e)})),this.norm.clear())}add(t){const e=this.size();r(t)?this._addString(t,e):this._addObject(t,e)}removeAt(t){this.records.splice(t,1);for(let e=t,s=this.size();e<s;e+=1)this.records[e].i-=1}size(){return this.records.length}_addString(t,e){if(!c(t)||h(t))return;let s={v:t,i:e,n:this.norm.get(t)};this.records.push(s)}_addObject(t,e){let s={i:e,$:{}};this.keys.forEach(((e,i)=>{let o=this.getFn(t,e);if(c(o))if(n(o)){let t=[];const e=[{nestedArrIndex:-1,value:o}];for(;e.length;){const{nestedArrIndex:s,value:i}=e.pop();if(c(i))if(r(i)&&!h(i)){let e={v:i,i:s,n:this.norm.get(i)};t.push(e)}else n(i)&&i.forEach(((t,s)=>{e.push({nestedArrIndex:s,value:t})}))}s.$[i]=t}else if(!h(o)){let t={v:o,n:this.norm.get(o)};s.$[i]=t}})),this.records.push(s)}toJSON(){return{keys:this.keys,records:this.records}}}function f(t,e,{getFn:s=l.getFn}={}){let n=new d({getFn:s});return n.setKeys(t),n.setCollection(e),n.create(),n}function g(t,e){const s=t.matches;e.matches=[],c(s)&&s.forEach((t=>{if(!c(t.indices)||!t.indices.length)return;const{indices:s,value:n}=t;let r={indices:s,value:n};t.key&&(r.key=t.key),t.idx>-1&&(r.refIndex=t.idx),e.matches.push(r)}))}function p(t,e){e.score=t.score}function M(t,{errors:e=0,currentLocation:s=0,expectedLocation:n=0,distance:r=l.distance}={}){const i=e/t.length,c=Math.abs(n-s);return r?i+c/r:c?1:i}const m=32;function y(t,e,s,{location:n=l.location,distance:r=l.distance,threshold:i=l.threshold,findAllMatches:c=l.findAllMatches,minMatchCharLength:h=l.minMatchCharLength,includeMatches:o=l.includeMatches}={}){if(e.length>m)throw new Error(`Pattern length exceeds max of ${m}.`);const a=e.length,u=t.length,d=Math.max(0,Math.min(n,u));let f=i,g=d;const p=[];if(o)for(let t=0;t<u;t+=1)p[t]=0;let y;for(;(y=t.indexOf(e,g))>-1;){let t=M(e,{currentLocation:y,expectedLocation:d,distance:r});if(f=Math.min(t,f),g=y+a,o){let t=0;for(;t<a;)p[y+t]=1,t+=1}}g=-1;let x=[],k=1,_=a+u;const v=1<<(a<=31?a-1:30);for(let n=0;n<a;n+=1){let i=0,h=_;for(;i<h;){M(e,{errors:n,currentLocation:d+h,expectedLocation:d,distance:r})<=f?i=h:_=h,h=Math.floor((_-i)/2+i)}_=h;let l=Math.max(1,d-h+1),m=c?u:Math.min(d+h,u)+a,y=Array(m+2);y[m+1]=(1<<n)-1;for(let i=m;i>=l;i-=1){let c=i-1,h=s[t.charAt(c)];if(h&&o&&(p[c]=1),y[i]=(y[i+1]<<1|1)&h,0!==n&&(y[i]|=(x[i+1]|x[i])<<1|1|x[i+1]),y[i]&v&&(k=M(e,{errors:n,currentLocation:c,expectedLocation:d,distance:r}),k<=f)){if(f=k,g=c,g<=d)break;l=Math.max(1,2*d-g)}}if(M(e,{errors:n+1,currentLocation:d,expectedLocation:d,distance:r})>f)break;x=y}let C={isMatch:g>=0,score:Math.max(.001,k)};return o&&(C.indices=function(t=[],e=l.minMatchCharLength){let s=[],n=-1,r=-1,i=0;for(let c=t.length;i<c;i+=1){let c=t[i];c&&-1===n?n=i:c||-1===n||(r=i-1,r-n+1>=e&&s.push([n,r]),n=-1)}return t[i-1]&&i-n>=e&&s.push([n,i-1]),s}(p,h)),C}function x(t){let e={},s=t.length;for(let n=0;n<s;n+=1)e[t.charAt(n)]=0;for(let n=0;n<s;n+=1)e[t.charAt(n)]|=1<<s-n-1;return e}class k{constructor(t,{location:e=l.location,threshold:s=l.threshold,distance:n=l.distance,includeMatches:r=l.includeMatches,findAllMatches:i=l.findAllMatches,minMatchCharLength:c=l.minMatchCharLength,isCaseSensitive:h=l.isCaseSensitive}={}){this.options={location:e,threshold:s,distance:n,includeMatches:r,findAllMatches:i,minMatchCharLength:c,isCaseSensitive:h},this.pattern=h?t:t.toLowerCase(),this.chunks=[];let o=0;for(;o<this.pattern.length;){let t=this.pattern.substring(o,o+m);this.chunks.push({pattern:t,alphabet:x(t)}),o+=m}}searchIn(t){const{isCaseSensitive:e,includeMatches:s}=this.options;if(e||(t=t.toLowerCase()),this.pattern===t){let e={isMatch:!0,score:0};return s&&(e.indices=[[0,t.length-1]]),e}const{location:n,distance:r,threshold:i,findAllMatches:c,minMatchCharLength:h}=this.options;let o=[],a=0,l=!1;this.chunks.forEach((({pattern:e,alphabet:u},d)=>{const{isMatch:f,score:g,indices:p}=y(t,e,u,{location:n+m*d,distance:r,threshold:i,findAllMatches:c,minMatchCharLength:h,includeMatches:s});f&&(l=!0),a+=g,f&&p&&(o=[...o,...p])}));let u={isMatch:l,score:l?a/this.chunks.length:1};return l&&s&&(u.indices=o),u}}class _{constructor(t){this.pattern=t}static isMultiMatch(t){return v(t,this.multiRegex)}static isSingleMatch(t){return v(t,this.singleRegex)}search(){}}function v(t,e){const s=t.match(e);return s?s[1]:null}class C extends _{constructor(t){super(t)}static get type(){return"exact"}static get multiRegex(){return/^'"(.*)"$/}static get singleRegex(){return/^'(.*)$/}search(t){let e,s=0;const n=[],r=this.pattern.length;for(;(e=t.indexOf(this.pattern,s))>-1;)s=e+r,n.push([e,s-1]);const i=!!n.length;return{isMatch:i,score:i?1:0,indices:n}}}class S extends _{constructor(t,{location:e=l.location,threshold:s=l.threshold,distance:n=l.distance,includeMatches:r=l.includeMatches,findAllMatches:i=l.findAllMatches,minMatchCharLength:c=l.minMatchCharLength,isCaseSensitive:h=l.isCaseSensitive}={}){super(t),this._bitapSearch=new k(t,{location:e,threshold:s,distance:n,includeMatches:r,findAllMatches:i,minMatchCharLength:c,isCaseSensitive:h})}static get type(){return"fuzzy"}static get multiRegex(){return/^"(.*)"$/}static get singleRegex(){return/^(.*)$/}search(t){return this._bitapSearch.searchIn(t)}}const L=[C,class extends _{constructor(t){super(t)}static get type(){return"prefix-exact"}static get multiRegex(){return/^\^"(.*)"$/}static get singleRegex(){return/^\^(.*)$/}search(t){const e=t.startsWith(this.pattern);return{isMatch:e,score:e?0:1,indices:[0,this.pattern.length-1]}}},class extends _{constructor(t){super(t)}static get type(){return"inverse-prefix-exact"}static get multiRegex(){return/^!\^"(.*)"$/}static get singleRegex(){return/^!\^(.*)$/}search(t){const e=!t.startsWith(this.pattern);return{isMatch:e,score:e?0:1,indices:[0,t.length-1]}}},class extends _{constructor(t){super(t)}static get type(){return"inverse-suffix-exact"}static get multiRegex(){return/^!"(.*)"\$$/}static get singleRegex(){return/^!(.*)\$$/}search(t){const e=!t.endsWith(this.pattern);return{isMatch:e,score:e?0:1,indices:[0,t.length-1]}}},class extends _{constructor(t){super(t)}static get type(){return"suffix-exact"}static get multiRegex(){return/^"(.*)"\$$/}static get singleRegex(){return/^(.*)\$$/}search(t){const e=t.endsWith(this.pattern);return{isMatch:e,score:e?0:1,indices:[t.length-this.pattern.length,t.length-1]}}},class extends _{constructor(t){super(t)}static get type(){return"inverse-exact"}static get multiRegex(){return/^!"(.*)"$/}static get singleRegex(){return/^!(.*)$/}search(t){const e=-1===t.indexOf(this.pattern);return{isMatch:e,score:e?0:1,indices:[0,t.length-1]}}},S],w=L.length,A=/ +(?=([^\"]*\"[^\"]*\")*[^\"]*$)/;const $=new Set([S.type,C.type]);class b{constructor(t,{isCaseSensitive:e=l.isCaseSensitive,includeMatches:s=l.includeMatches,minMatchCharLength:n=l.minMatchCharLength,findAllMatches:r=l.findAllMatches,location:i=l.location,threshold:c=l.threshold,distance:h=l.distance}={}){this.query=null,this.options={isCaseSensitive:e,includeMatches:s,minMatchCharLength:n,findAllMatches:r,location:i,threshold:c,distance:h},this.pattern=e?t:t.toLowerCase(),this.query=function(t,e={}){return t.split("|").map((t=>{let s=t.trim().split(A).filter((t=>t&&!!t.trim())),n=[];for(let t=0,r=s.length;t<r;t+=1){const r=s[t];let i=!1,c=-1;for(;!i&&++c<w;){const t=L[c];let s=t.isMultiMatch(r);s&&(n.push(new t(s,e)),i=!0)}if(!i)for(c=-1;++c<w;){const t=L[c];let s=t.isSingleMatch(r);if(s){n.push(new t(s,e));break}}}return n}))}(this.pattern,this.options)}static condition(t,e){return e.useExtendedSearch}searchIn(t){const e=this.query;if(!e)return{isMatch:!1,score:1};const{includeMatches:s,isCaseSensitive:n}=this.options;t=n?t:t.toLowerCase();let r=0,i=[],c=0;for(let n=0,h=e.length;n<h;n+=1){const h=e[n];i.length=0,r=0;for(let e=0,n=h.length;e<n;e+=1){const n=h[e],{isMatch:o,indices:a,score:l}=n.search(t);if(!o){c=0,r=0,i.length=0;break}if(r+=1,c+=l,s){const t=n.constructor.type;$.has(t)?i=[...i,...a]:i.push(a)}}if(r){let t={isMatch:!0,score:c/r};return s&&(t.indices=i),t}}return{isMatch:!1,score:1}}}const E=[];function I(t,e){for(let s=0,n=E.length;s<n;s+=1){let n=E[s];if(n.condition(t,e))return new n(t,e)}return new k(t,e)}const O="$and",R="$or",F=t=>!(!t[O]&&!t[R]),j=t=>({[O]:Object.keys(t).map((e=>({[e]:t[e]})))});function N(t,e,{auto:s=!0}={}){const i=t=>{let c=Object.keys(t);if(c.length>1&&!F(t))return i(j(t));let h=c[0];if((t=>!n(t)&&"object"==typeof t&&!F(t))(t)){const n=t[h];if(!r(n))throw new Error((t=>"Invalid value for key "+t)(h));const i={key:h,pattern:n};return s&&(i.searcher=I(n,e)),i}let o={children:[],operator:h};return c.forEach((e=>{const s=t[e];n(s)&&s.forEach((t=>{o.children.push(i(t))}))})),o};return F(t)||(t=j(t)),i(t)}class z{constructor(t,e={},s){this.options={...l,...e},this.options.useExtendedSearch,this._keyStore=new a(this.options.keys),this.setCollection(t,s)}setCollection(t,e){if(this._docs=t,e&&!(e instanceof d))throw new Error("Incorrect 'index' type");this._myIndex=e||f(this._keyStore.keys(),this._docs,{getFn:this.options.getFn})}add(t){c(t)&&(this._docs.push(t),this._myIndex.add(t))}removeAt(t){this._docs.splice(t,1),this._myIndex.removeAt(t)}getIndex(){return this._myIndex}search(t,{limit:e=-1}={}){const{includeMatches:s,includeScore:n,shouldSort:c,sortFn:h}=this.options;let o=r(t)?r(this._docs[0])?this._searchStringList(t):this._searchObjectList(t):this._searchLogical(t);return function(t,e){t.forEach((t=>{let s=1;t.matches.forEach((({key:t,norm:n,score:r})=>{const i=e.get(t,"weight");s*=Math.pow(0===r&&i?Number.EPSILON:r,(i||1)*n)})),t.score=s}))}(o,this._keyStore),c&&o.sort(h),i(e)&&e>-1&&(o=o.slice(0,e)),function(t,e,{includeMatches:s=l.includeMatches,includeScore:n=l.includeScore}={}){const r=[];s&&r.push(g);n&&r.push(p);return t.map((t=>{const{idx:s}=t,n={item:e[s],refIndex:s};return r.length&&r.forEach((e=>{e(t,n)})),n}))}(o,this._docs,{includeMatches:s,includeScore:n})}_searchStringList(t){const e=I(t,this.options),{records:s}=this._myIndex,n=[];return s.forEach((({v:t,i:s,n:r})=>{if(!c(t))return;const{isMatch:i,score:h,indices:o}=e.searchIn(t);i&&n.push({item:t,idx:s,matches:[{score:h,value:t,norm:r,indices:o}]})})),n}_searchLogical(t){const e=N(t,this.options),{keys:s,records:n}=this._myIndex,r={},i=[],h=(t,e,n)=>{if(!t.children){const{key:n,searcher:r}=t,i=e[s.indexOf(n)];return this._findMatches({key:n,value:i,searcher:r})}{const s=t.operator;let c=[];for(let r=0;r<t.children.length;r+=1){let i=t.children[r],o=h(i,e,n);if(o&&o.length){if(c.push({idx:n,item:e,matches:o}),s===R)break}else if(s===O){c.length=0;break}}c.length&&(r[n]||(r[n]={idx:n,item:e,matches:[]},i.push(r[n])),c.forEach((({matches:t})=>{r[n].matches.push(...t)})))}};return n.forEach((({$:t,i:s})=>{c(t)&&h(e,t,s)})),i}_searchObjectList(t){const e=I(t,this.options),{keys:s,records:n}=this._myIndex,r=[];return n.forEach((({$:t,i:n})=>{if(!c(t))return;let i=[];s.forEach(((s,n)=>{i.push(...this._findMatches({key:s,value:t[n],searcher:e}))})),i.length&&r.push({idx:n,item:t,matches:i})})),r}_findMatches({key:t,value:e,searcher:s}){if(!c(e))return[];let r=[];if(n(e))e.forEach((({v:e,i:n,n:i})=>{if(!c(e))return;const{isMatch:h,score:o,indices:a}=s.searchIn(e);h&&r.push({score:o,key:t,value:e,idx:n,norm:i,indices:a})}));else{const{v:n,n:i}=e,{isMatch:c,score:h,indices:o}=s.searchIn(n);c&&r.push({score:h,key:t,value:n,norm:i,indices:o})}return r}}z.version="6.0.0",z.createIndex=f,z.parseIndex=function(t,{getFn:e=l.getFn}={}){const{keys:s,records:n}=t;let r=new d({getFn:e});return r.setKeys(s),r.setRecords(n),r},z.config=l,z.parseQuery=N,function(...t){E.push(...t)}(b);const q=z}}]);
//# sourceMappingURL=chunk.38d3977ff7f099485538.js.map