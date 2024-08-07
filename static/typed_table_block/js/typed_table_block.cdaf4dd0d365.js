(()=>{"use strict";var t,e={7595:(t,e,n)=>{var i=n(4327),o=n(9675),s=n(4545);class l{constructor(t,e,n,o,s){this.blockDef=t,this.type=t.name,this.caption="",this.columns=[],this.rows=[],this.columnCountIncludingDeleted=0,this.rowCountIncludingDeleted=0,this.prefix=n,this.childBlockDefsByName={},this.blockDef.childBlockDefs.forEach((t=>{this.childBlockDefsByName[t.name]=t}));const l=this.blockDef.meta.strings,a=`${(0,i.Z)(n)}-caption`,d=$(`\n      <div class="typed-table-block ${(0,i.Z)(this.blockDef.meta.classname||"")}">\n        <div class="w-field__wrapper" data-field-wrapper>\n          <label class="w-field__label" for="${a}">\n            ${l.CAPTION}\n          </label>\n          <div class="w-field w-field--char_field w-field--text_input" data-field>\n            <div class="w-field__help" data-field-help>\n              <div class="help">\n                ${l.CAPTION_HELP_TEXT}\n              </div>\n            </div>\n            <div class="w-field__input" data-field-input>\n              <input type="text" id="${a}" name="${a}" value="" />\n              <span></span>\n            </div>\n          </div>\n        </div>\n        <input type="hidden" name="${(0,i.Z)(n)}-column-count" data-column-count value="0">\n        <input type="hidden" name="${(0,i.Z)(n)}-row-count" data-row-count value="0">\n        <div data-deleted-fields></div>\n        <div class="typed-table-block__wrapper">\n          <table>\n            <thead>\n              <tr>\n                <th></th>\n                <th class="control-cell">\n                  <button type="button" class="button button-small button-secondary append-column" data-append-column>\n                    ${(0,i.Z)(l.ADD_COLUMN)}\n                  </button>\n                </th>\n              </tr>\n            </thead>\n            <tbody>\n            </tbody>\n            <tfoot>\n              <tr>\n                <td class="control-cell">\n                  <button\n                    type="button"\n                    class="button button-small button-secondary button--icon text-replace prepend-row"\n                    data-add-row\n                    aria-label="${(0,i.Z)(l.ADD_ROW)}"\n                    title="${(0,i.Z)(l.ADD_ROW)}"\n                  >\n                    <svg class="icon icon-plus icon" aria-hidden="true">\n                      <use href="#icon-plus"></use>\n                    </svg>\n                  </button></td>\n              </tr>\n            </tfoot>\n          </table>\n        </div>\n      </div>\n    `);$(e).replaceWith(d),this.container=d,this.captionInput=d.find(`#${a}`).get(0),this.thead=d.find("table > thead").get(0),this.tbody=d.find("table > tbody").get(0),this.columnCountInput=d.find("input[data-column-count]").get(0),this.rowCountInput=d.find("input[data-row-count]").get(0),this.deletedFieldsContainer=d.find("[data-deleted-fields]").get(0),this.appendColumnButton=d.find("button[data-append-column]"),this.addRowButton=d.find("button[data-add-row]"),this.addRowButton.hide(),this.blockDef.meta.helpText&&d.append(`\n        <div class="c-sf-help">\n          <div class="help">\n            ${this.blockDef.meta.helpText}\n          </div>\n        </div>\n      `),this.addColumnCallback=null,this.addColumnMenu=$('<ul class="add-column-menu"></ul>'),this.blockDef.childBlockDefs.forEach((t=>{const e=$('<button type="button" class="button button-small"></button>').text(t.meta.label);e.on("click",(()=>{this.addColumnCallback&&this.addColumnCallback(t),this.hideAddColumnMenu()}));const n=$("<li></li>").append(e);this.addColumnMenu.append(n)})),this.addColumnMenuBaseElement=null,this.appendColumnButton.on("click",(()=>{this.toggleAddColumnMenu(this.appendColumnButton,(t=>{this.insertColumn(this.columns.length,t,{addInitialRow:!0})}))})),this.addRowButton.on("click",(()=>{this.insertRow(this.rows.length)})),this.setState(o),s&&this.setError(s)}showAddColumnMenu(t,e){this.addColumnMenuBaseElement=t,t.after(this.addColumnMenu),this.addColumnMenu.show(),this.addColumnCallback=e}hideAddColumnMenu(){this.addColumnMenu.hide(),this.addColumnMenuBaseElement=null}toggleAddColumnMenu(t,e){this.addColumnMenuBaseElement===t?this.hideAddColumnMenu():this.showAddColumnMenu(t,e)}clear(){this.setCaption(""),this.columns=[],this.rows=[],this.columnCountIncludingDeleted=0,this.columnCountInput.value=0,this.rowCountIncludingDeleted=0,this.rowCountInput.value=0,this.deletedFieldsContainer.replaceChildren();const t=this.thead.children[0];t.replaceChildren(t.firstElementChild,t.lastElementChild),this.appendColumnButton.text(this.blockDef.meta.strings.ADD_COLUMN).removeClass("button--icon text-replace white").removeAttr("aria-label").removeAttr("title"),this.tbody.replaceChildren(),this.addRowButton.hide()}setCaption(t){this.caption=t,this.captionInput.value=t}insertColumn(t,e,n){const s={blockDef:e,position:t,id:this.columnCountIncludingDeleted};this.columnCountIncludingDeleted+=1,(0,o.y)(t,this.columns.length).forEach((t=>{this.columns[t].position+=1,this.columns[t].positionInput.value=this.columns[t].position})),this.columns.splice(t,0,s),this.columnCountInput.value=this.columnCountIncludingDeleted;const l=this.thead.children[0],a=l.children,d=document.createElement("th");l.insertBefore(d,a[t+1]),s.typeInput=document.createElement("input"),s.typeInput.type="hidden",s.typeInput.name=this.prefix+"-column-"+s.id+"-type",s.typeInput.value=e.name,d.appendChild(s.typeInput),s.positionInput=document.createElement("input"),s.positionInput.type="hidden",s.positionInput.name=this.prefix+"-column-"+s.id+"-order",s.positionInput.value=t,d.appendChild(s.positionInput),s.deletedInput=document.createElement("input"),s.deletedInput.type="hidden",s.deletedInput.name=this.prefix+"-column-"+s.id+"-deleted",s.deletedInput.value="",this.deletedFieldsContainer.appendChild(s.deletedInput);const u=$(`<button type="button"\n      class="button button-secondary button-small button--icon text-replace prepend-column"\n      aria-label="${(0,i.Z)(this.blockDef.meta.strings.INSERT_COLUMN)}"\n      title="${(0,i.Z)(this.blockDef.meta.strings.INSERT_COLUMN)}">\n        <svg class="icon icon-plus icon" aria-hidden="true"><use href="#icon-plus"></use></svg>\n      </button>`);$(d).append(u),u.on("click",(()=>{this.toggleAddColumnMenu(u,(t=>{this.insertColumn(s.position,t,{addInitialRow:!0})}))})),s.headingInput=document.createElement("input"),s.headingInput.type="text",s.headingInput.name=this.prefix+"-column-"+s.id+"-heading",s.headingInput.className="column-heading",s.headingInput.placeholder=this.blockDef.meta.strings.COLUMN_HEADING,d.appendChild(s.headingInput);const c=$(`<button type="button"\n      class="button button-secondary button-small button--icon text-replace no delete-column"\n      aria-label="${(0,i.Z)(this.blockDef.meta.strings.DELETE_COLUMN)}"\n      title="${(0,i.Z)(this.blockDef.meta.strings.DELETE_COLUMN)}">\n        <svg class="icon icon-bin icon" aria-hidden="true"><use href="#icon-bin"></use></svg>\n      </button>`);$(d).append(c),c.on("click",(()=>{this.deleteColumn(s.position)}));const r=this.blockDef.childBlockDefaultStates[e.name];return Array.from(this.tbody.children).forEach(((e,n)=>{const i=this.rows[n],o=e.children,l=document.createElement("td");e.insertBefore(l,o[t+1]);const a=this.initCell(l,s,i,r);i.blocks.splice(t,0,a)})),this.addRowButton.show(),this.appendColumnButton.html('<svg class="icon icon-plus icon" aria-hidden="true"><use href="#icon-plus"></use></svg>').addClass("button--icon text-replace white").attr("aria-label",this.blockDef.meta.strings.ADD_COLUMN).addClass("button--icon text-replace white").attr("aria-label",this.blockDef.meta.strings.ADD_COLUMN).attr("title",this.blockDef.meta.strings.ADD_COLUMN),n&&n.addInitialRow&&0===this.tbody.children.length&&this.insertRow(0),s}deleteColumn(t){this.columns[t].deletedInput.value="1";const e=this.thead.children[0],n=e.children;e.removeChild(n[t+1]),Array.from(this.tbody.children).forEach(((e,n)=>{const i=e.children;e.removeChild(i[t+1]),this.rows[n].blocks.splice(t,1)})),this.columns.splice(t,1),(0,o.y)(t,this.columns.length).forEach((t=>{this.columns[t].position-=1,this.columns[t].positionInput.value=this.columns[t].position})),0===this.columns.length&&this.clear()}insertRow(t,e){const n=document.createElement("tr"),s={blocks:[],position:t,id:this.rowCountIncludingDeleted};if(t<this.rows.length){const e=this.tbody.children[t];this.tbody.insertBefore(n,e)}else this.tbody.appendChild(n);this.rows.splice(t,0,s),this.rowCountIncludingDeleted+=1,this.rowCountInput.value=this.rowCountIncludingDeleted;const l=document.createElement("td");l.className="control-cell",n.appendChild(l);const a=$(`<button type="button"\n      class="button button-secondary button-small button--icon text-replace prepend-row"\n      aria-label="${(0,i.Z)(this.blockDef.meta.strings.INSERT_ROW)}"\n      title="${(0,i.Z)(this.blockDef.meta.strings.INSERT_ROW)}">\n        <svg class="icon icon-plus icon" aria-hidden="true"><use href="#icon-plus"></use></svg>\n      </button>`);$(l).append(a),a.on("click",(()=>{this.insertRow(s.position)})),this.columns.forEach(((t,i)=>{let o;o=e?e[i]:this.blockDef.childBlockDefaultStates[t.blockDef.name];const l=document.createElement("td");n.appendChild(l),s.blocks[i]=this.initCell(l,t,s,o)}));const d=document.createElement("td");d.className="control-cell",n.appendChild(d),s.positionInput=document.createElement("input"),s.positionInput.type="hidden",s.positionInput.name=this.prefix+"-row-"+s.id+"-order",s.positionInput.value=s.position,d.appendChild(s.positionInput);const u=$(`<button type="button"\n      class="button button-secondary button-small button--icon text-replace no delete-row"\n      aria-label="${(0,i.Z)(this.blockDef.meta.strings.DELETE_ROW)}"\n      title="${(0,i.Z)(this.blockDef.meta.strings.DELETE_ROW)}">\n        <svg class="icon icon-bin icon" aria-hidden="true"><use href="#icon-bin"></use></svg>\n      </button>`);return $(d).append(u),u.on("click",(()=>{this.deleteRow(s.position)})),s.deletedInput=document.createElement("input"),s.deletedInput.type="hidden",s.deletedInput.name=this.prefix+"-row-"+s.id+"-deleted",s.deletedInput.value="",this.deletedFieldsContainer.appendChild(s.deletedInput),(0,o.y)(t+1,this.rows.length).forEach((t=>{this.rows[t].position+=1,this.rows[t].positionInput.value=this.rows[t].position})),s}deleteRow(t){this.rows[t].deletedInput.value="1";const e=this.tbody.children[t];this.tbody.removeChild(e),this.rows.splice(t,1),(0,o.y)(t,this.rows.length).forEach((t=>{this.rows[t].position-=1,this.rows[t].positionInput.value=this.rows[t].position}))}initCell(t,e,n,i){const o=document.createElement("div");t.appendChild(o);const s=this.prefix+"-cell-"+n.id+"-"+e.id;return e.blockDef.render(o,s,i,null)}setState(t){this.clear(),t&&(t.columns.forEach(((t,e)=>{const n=this.childBlockDefsByName[t.type];this.insertColumn(e,n).headingInput.value=t.heading})),t.rows.forEach(((t,e)=>{this.insertRow(e,t.values)})),this.setCaption(t.caption))}setError(t){if(!t)return;const e=this.container[0];if((0,s.$)(e),t.messages&&(0,s.U)(e,t.messages),t.blockErrors)for(const[e,n]of Object.entries(t.blockErrors))for(const[t,i]of Object.entries(n))this.rows[e].blocks[t].setError(i)}getState(){return{columns:this.getColumnStates(),rows:this.rows.map((t=>({values:t.blocks.map((t=>t.getState()))}))),caption:this.caption}}getDuplicatedState(){return{columns:this.getColumnStates(),rows:this.rows.map((t=>({values:t.blocks.map((t=>void 0===t.getDuplicatedState?t.getState():t.getDuplicatedState()))})))}}getValue(){return{columns:this.getColumnStates(),rows:this.rows.map((t=>({values:t.blocks.map((t=>t.getValue()))}))),caption:this.caption}}getColumnStates(){return this.columns.map((t=>({type:t.blockDef.name,heading:t.headingInput.value})))}getTextLabel(t){const e=t&&t.maxLength;let n="";for(const t of this.rows)for(const i of t.blocks)if(i.getTextLabel){const t=i.getTextLabel({maxLength:e});if(t)if(n){const i=n+", "+t;if(e&&i.length>e-1)return n.endsWith("…")||(n+="…"),n;n=i}else n=t}return n}focus(t){this.columns.length?this.rows.length?this.rows[0].blocks[0].focus(t):this.addRowButton.focus():this.appendColumnButton.focus()}}window.telepath.register("wagtail.contrib.typed_table_block.blocks.TypedTableBlock",class{constructor(t,e,n,i){this.name=t,this.childBlockDefs=e,this.childBlockDefaultStates=n,this.meta=i}render(t,e,n,i){return new l(this,t,e,n,i)}})}},n={};function i(t){var o=n[t];if(void 0!==o)return o.exports;var s=n[t]={exports:{}};return e[t](s,s.exports,i),s.exports}i.m=e,t=[],i.O=(e,n,o,s)=>{if(!n){var l=1/0;for(c=0;c<t.length;c++){for(var[n,o,s]=t[c],a=!0,d=0;d<n.length;d++)(!1&s||l>=s)&&Object.keys(i.O).every((t=>i.O[t](n[d])))?n.splice(d--,1):(a=!1,s<l&&(l=s));if(a){t.splice(c--,1);var u=o();void 0!==u&&(e=u)}}return e}s=s||0;for(var c=t.length;c>0&&t[c-1][2]>s;c--)t[c]=t[c-1];t[c]=[n,o,s]},i.n=t=>{var e=t&&t.__esModule?()=>t.default:()=>t;return i.d(e,{a:e}),e},i.d=(t,e)=>{for(var n in e)i.o(e,n)&&!i.o(t,n)&&Object.defineProperty(t,n,{enumerable:!0,get:e[n]})},i.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(t){if("object"==typeof window)return window}}(),i.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),i.r=t=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},i.j=702,(()=>{var t={702:0};i.O.j=e=>0===t[e];var e=(e,n)=>{var o,s,[l,a,d]=n,u=0;if(l.some((e=>0!==t[e]))){for(o in a)i.o(a,o)&&(i.m[o]=a[o]);if(d)var c=d(i)}for(e&&e(n);u<l.length;u++)s=l[u],i.o(t,s)&&t[s]&&t[s][0](),t[s]=0;return i.O(c)},n=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];n.forEach(e.bind(null,0)),n.push=e.bind(null,n.push.bind(n))})();var o=i.O(void 0,[321],(()=>i(7595)));o=i.O(o)})();