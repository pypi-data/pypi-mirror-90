(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[5],{1724:function(t,e,o){"use strict";function r(t){return t&&"object"===typeof t&&"default"in t?t.default:t}Object.defineProperty(e,"__esModule",{value:!0});var n=r(o(4)),i=r(o(186)),a=r(o(51)),l=r(o(2464)),s=o(0),c=r(o(439)),u="object"===typeof performance&&"function"===typeof performance.now?function(){return performance.now()}:function(){return Date.now()};function d(t){cancelAnimationFrame(t.id)}function f(t,e){var o=u();var r={id:requestAnimationFrame((function n(){u()-o>=e?t.call(null):r.id=requestAnimationFrame(n)}))};return r}var h=-1;var m=null;function p(t){if(void 0===t&&(t=!1),null===m||t){var e=document.createElement("div"),o=e.style;o.width="50px",o.height="50px",o.overflow="scroll",o.direction="rtl";var r=document.createElement("div"),n=r.style;return n.width="100px",n.height="100px",e.appendChild(r),document.body.appendChild(e),e.scrollLeft>0?m="positive-descending":(e.scrollLeft=1,m=0===e.scrollLeft?"negative":"positive-ascending"),document.body.removeChild(e),m}return m}var g=function(t){var e=t.columnIndex;t.data;return t.rowIndex+":"+e};function v(t){var e,o,r=t.getColumnOffset,c=t.getColumnStartIndexForOffset,u=t.getColumnStopIndexForStartIndex,m=t.getColumnWidth,v=t.getEstimatedTotalHeight,I=t.getEstimatedTotalWidth,w=t.getOffsetForColumnAndAlignment,M=t.getOffsetForRowAndAlignment,x=t.getRowHeight,C=t.getRowOffset,_=t.getRowStartIndexForOffset,R=t.getRowStopIndexForStartIndex,y=t.initInstanceProps,T=t.shouldResetStyleCacheOnItemSizeChange,z=t.validateProps;return o=e=function(t){function e(e){var o;return(o=t.call(this,e)||this)._instanceProps=y(o.props,a(a(o))),o._resetIsScrollingTimeoutId=null,o._outerRef=void 0,o.state={instance:a(a(o)),isScrolling:!1,horizontalScrollDirection:"forward",scrollLeft:"number"===typeof o.props.initialScrollLeft?o.props.initialScrollLeft:0,scrollTop:"number"===typeof o.props.initialScrollTop?o.props.initialScrollTop:0,scrollUpdateWasRequested:!1,verticalScrollDirection:"forward"},o._callOnItemsRendered=void 0,o._callOnItemsRendered=l((function(t,e,r,n,i,a,l,s){return o.props.onItemsRendered({overscanColumnStartIndex:t,overscanColumnStopIndex:e,overscanRowStartIndex:r,overscanRowStopIndex:n,visibleColumnStartIndex:i,visibleColumnStopIndex:a,visibleRowStartIndex:l,visibleRowStopIndex:s})})),o._callOnScroll=void 0,o._callOnScroll=l((function(t,e,r,n,i){return o.props.onScroll({horizontalScrollDirection:r,scrollLeft:t,scrollTop:e,verticalScrollDirection:n,scrollUpdateWasRequested:i})})),o._getItemStyle=void 0,o._getItemStyle=function(t,e){var n,i=o.props,a=i.columnWidth,l=i.direction,s=i.rowHeight,c=o._getItemStyleCache(T&&a,T&&l,T&&s),u=t+":"+e;if(c.hasOwnProperty(u))n=c[u];else{var d=r(o.props,e,o._instanceProps),f="rtl"===l;c[u]=n={position:"absolute",left:f?void 0:d,right:f?d:void 0,top:C(o.props,t,o._instanceProps),height:x(o.props,t,o._instanceProps),width:m(o.props,e,o._instanceProps)}}return n},o._getItemStyleCache=void 0,o._getItemStyleCache=l((function(t,e,o){return{}})),o._onScroll=function(t){var e=t.currentTarget,r=e.clientHeight,n=e.clientWidth,i=e.scrollLeft,a=e.scrollTop,l=e.scrollHeight,s=e.scrollWidth;o.setState((function(t){if(t.scrollLeft===i&&t.scrollTop===a)return null;var e=o.props.direction,c=i;if("rtl"===e)switch(p()){case"negative":c=-i;break;case"positive-descending":c=s-n-i}c=Math.max(0,Math.min(c,s-n));var u=Math.max(0,Math.min(a,l-r));return{isScrolling:!0,horizontalScrollDirection:t.scrollLeft<i?"forward":"backward",scrollLeft:c,scrollTop:u,verticalScrollDirection:t.scrollTop<a?"forward":"backward",scrollUpdateWasRequested:!1}}),o._resetIsScrollingDebounced)},o._outerRefSetter=function(t){var e=o.props.outerRef;o._outerRef=t,"function"===typeof e?e(t):null!=e&&"object"===typeof e&&e.hasOwnProperty("current")&&(e.current=t)},o._resetIsScrollingDebounced=function(){null!==o._resetIsScrollingTimeoutId&&d(o._resetIsScrollingTimeoutId),o._resetIsScrollingTimeoutId=f(o._resetIsScrolling,150)},o._resetIsScrolling=function(){o._resetIsScrollingTimeoutId=null,o.setState({isScrolling:!1},(function(){o._getItemStyleCache(-1)}))},o}i(e,t),e.getDerivedStateFromProps=function(t,e){return S(t,e),z(t),null};var o=e.prototype;return o.scrollTo=function(t){var e=t.scrollLeft,o=t.scrollTop;void 0!==e&&(e=Math.max(0,e)),void 0!==o&&(o=Math.max(0,o)),this.setState((function(t){return void 0===e&&(e=t.scrollLeft),void 0===o&&(o=t.scrollTop),t.scrollLeft===e&&t.scrollTop===o?null:{horizontalScrollDirection:t.scrollLeft<e?"forward":"backward",scrollLeft:e,scrollTop:o,scrollUpdateWasRequested:!0,verticalScrollDirection:t.scrollTop<o?"forward":"backward"}}),this._resetIsScrollingDebounced)},o.scrollToItem=function(t){var e=t.align,o=void 0===e?"auto":e,r=t.columnIndex,n=t.rowIndex,i=this.props,a=i.columnCount,l=i.height,s=i.rowCount,c=i.width,u=this.state,d=u.scrollLeft,f=u.scrollTop,m=function(t){if(void 0===t&&(t=!1),-1===h||t){var e=document.createElement("div"),o=e.style;o.width="50px",o.height="50px",o.overflow="scroll",document.body.appendChild(e),h=e.offsetWidth-e.clientWidth,document.body.removeChild(e)}return h}();void 0!==r&&(r=Math.max(0,Math.min(r,a-1))),void 0!==n&&(n=Math.max(0,Math.min(n,s-1)));var p=v(this.props,this._instanceProps),g=I(this.props,this._instanceProps)>c?m:0,S=p>l?m:0;this.scrollTo({scrollLeft:void 0!==r?w(this.props,r,o,d,this._instanceProps,S):d,scrollTop:void 0!==n?M(this.props,n,o,f,this._instanceProps,g):f})},o.componentDidMount=function(){var t=this.props,e=t.initialScrollLeft,o=t.initialScrollTop;if(null!=this._outerRef){var r=this._outerRef;"number"===typeof e&&(r.scrollLeft=e),"number"===typeof o&&(r.scrollTop=o)}this._callPropsCallbacks()},o.componentDidUpdate=function(){var t=this.props.direction,e=this.state,o=e.scrollLeft,r=e.scrollTop;if(e.scrollUpdateWasRequested&&null!=this._outerRef){var n=this._outerRef;if("rtl"===t)switch(p()){case"negative":n.scrollLeft=-o;break;case"positive-ascending":n.scrollLeft=o;break;default:var i=n.clientWidth,a=n.scrollWidth;n.scrollLeft=a-i-o}else n.scrollLeft=Math.max(0,o);n.scrollTop=Math.max(0,r)}this._callPropsCallbacks()},o.componentWillUnmount=function(){null!==this._resetIsScrollingTimeoutId&&d(this._resetIsScrollingTimeoutId)},o.render=function(){var t=this.props,e=t.children,o=t.className,r=t.columnCount,i=t.direction,a=t.height,l=t.innerRef,c=t.innerElementType,u=t.innerTagName,d=t.itemData,f=t.itemKey,h=void 0===f?g:f,m=t.outerElementType,p=t.outerTagName,S=t.rowCount,w=t.style,M=t.useIsScrolling,x=t.width,C=this.state.isScrolling,_=this._getHorizontalRangeToRender(),R=_[0],y=_[1],T=this._getVerticalRangeToRender(),z=T[0],O=T[1],b=[];if(r>0&&S)for(var P=z;P<=O;P++)for(var W=R;W<=y;W++)b.push(s.createElement(e,{columnIndex:W,data:d,isScrolling:M?C:void 0,key:h({columnIndex:W,data:d,rowIndex:P}),rowIndex:P,style:this._getItemStyle(P,W)}));var D=v(this.props,this._instanceProps),F=I(this.props,this._instanceProps);return s.createElement(m||p||"div",{className:o,onScroll:this._onScroll,ref:this._outerRefSetter,style:n({position:"relative",height:a,width:x,overflow:"auto",WebkitOverflowScrolling:"touch",willChange:"transform",direction:i},w)},s.createElement(c||u||"div",{children:b,ref:l,style:{height:D,pointerEvents:C?"none":void 0,width:F}}))},o._callPropsCallbacks=function(){var t=this.props,e=t.columnCount,o=t.onItemsRendered,r=t.onScroll,n=t.rowCount;if("function"===typeof o&&e>0&&n>0){var i=this._getHorizontalRangeToRender(),a=i[0],l=i[1],s=i[2],c=i[3],u=this._getVerticalRangeToRender(),d=u[0],f=u[1],h=u[2],m=u[3];this._callOnItemsRendered(a,l,d,f,s,c,h,m)}if("function"===typeof r){var p=this.state,g=p.horizontalScrollDirection,v=p.scrollLeft,S=p.scrollTop,I=p.scrollUpdateWasRequested,w=p.verticalScrollDirection;this._callOnScroll(v,S,g,w,I)}},o._getHorizontalRangeToRender=function(){var t=this.props,e=t.columnCount,o=t.overscanColumnCount,r=t.overscanColumnsCount,n=t.overscanCount,i=t.rowCount,a=this.state,l=a.horizontalScrollDirection,s=a.isScrolling,d=a.scrollLeft,f=o||r||n||1;if(0===e||0===i)return[0,0,0,0];var h=c(this.props,d,this._instanceProps),m=u(this.props,h,d,this._instanceProps),p=s&&"backward"!==l?1:Math.max(1,f),g=s&&"forward"!==l?1:Math.max(1,f);return[Math.max(0,h-p),Math.max(0,Math.min(e-1,m+g)),h,m]},o._getVerticalRangeToRender=function(){var t=this.props,e=t.columnCount,o=t.overscanCount,r=t.overscanRowCount,n=t.overscanRowsCount,i=t.rowCount,a=this.state,l=a.isScrolling,s=a.verticalScrollDirection,c=a.scrollTop,u=r||n||o||1;if(0===e||0===i)return[0,0,0,0];var d=_(this.props,c,this._instanceProps),f=R(this.props,d,c,this._instanceProps),h=l&&"backward"!==s?1:Math.max(1,u),m=l&&"forward"!==s?1:Math.max(1,u);return[Math.max(0,d-h),Math.max(0,Math.min(i-1,f+m)),d,f]},e}(s.PureComponent),e.defaultProps={direction:"ltr",itemData:void 0,useIsScrolling:!1},o}var S=function(t,e){t.children,t.direction,t.height,t.innerTagName,t.outerTagName,t.overscanColumnsCount,t.overscanCount,t.overscanRowsCount,t.width,e.instance},I=function(t,e){var o=t.rowCount,r=e.rowMetadataMap,n=e.estimatedRowHeight,i=e.lastMeasuredRowIndex,a=0;if(i>=o&&(i=o-1),i>=0){var l=r[i];a=l.offset+l.size}return a+(o-i-1)*n},w=function(t,e){var o=t.columnCount,r=e.columnMetadataMap,n=e.estimatedColumnWidth,i=e.lastMeasuredColumnIndex,a=0;if(i>=o&&(i=o-1),i>=0){var l=r[i];a=l.offset+l.size}return a+(o-i-1)*n},M=function(t,e,o,r){var n,i,a;if("column"===t?(n=r.columnMetadataMap,i=e.columnWidth,a=r.lastMeasuredColumnIndex):(n=r.rowMetadataMap,i=e.rowHeight,a=r.lastMeasuredRowIndex),o>a){var l=0;if(a>=0){var s=n[a];l=s.offset+s.size}for(var c=a+1;c<=o;c++){var u=i(c);n[c]={offset:l,size:u},l+=u}"column"===t?r.lastMeasuredColumnIndex=o:r.lastMeasuredRowIndex=o}return n[o]},x=function(t,e,o,r){var n,i;return"column"===t?(n=o.columnMetadataMap,i=o.lastMeasuredColumnIndex):(n=o.rowMetadataMap,i=o.lastMeasuredRowIndex),(i>0?n[i].offset:0)>=r?C(t,e,o,i,0,r):_(t,e,o,Math.max(0,i),r)},C=function(t,e,o,r,n,i){for(;n<=r;){var a=n+Math.floor((r-n)/2),l=M(t,e,a,o).offset;if(l===i)return a;l<i?n=a+1:l>i&&(r=a-1)}return n>0?n-1:0},_=function(t,e,o,r,n){for(var i="column"===t?e.columnCount:e.rowCount,a=1;r<i&&M(t,e,r,o).offset<n;)r+=a,a*=2;return C(t,e,o,Math.min(r,i-1),Math.floor(r/2),n)},R=function(t,e,o,r,n,i,a){var l="column"===t?e.width:e.height,s=M(t,e,o,i),c="column"===t?w(e,i):I(e,i),u=Math.max(0,Math.min(c-l,s.offset)),d=Math.max(0,s.offset-l+a+s.size);switch("smart"===r&&(r=n>=d-l&&n<=u+l?"auto":"center"),r){case"start":return u;case"end":return d;case"center":return Math.round(d+(u-d)/2);case"auto":default:return n>=d&&n<=u?n:d>u||n<d?d:u}},y=v({getColumnOffset:function(t,e,o){return M("column",t,e,o).offset},getColumnStartIndexForOffset:function(t,e,o){return x("column",t,o,e)},getColumnStopIndexForStartIndex:function(t,e,o,r){for(var n=t.columnCount,i=t.width,a=M("column",t,e,r),l=o+i,s=a.offset+a.size,c=e;c<n-1&&s<l;)c++,s+=M("column",t,c,r).size;return c},getColumnWidth:function(t,e,o){return o.columnMetadataMap[e].size},getEstimatedTotalHeight:I,getEstimatedTotalWidth:w,getOffsetForColumnAndAlignment:function(t,e,o,r,n,i){return R("column",t,e,o,r,n,i)},getOffsetForRowAndAlignment:function(t,e,o,r,n,i){return R("row",t,e,o,r,n,i)},getRowOffset:function(t,e,o){return M("row",t,e,o).offset},getRowHeight:function(t,e,o){return o.rowMetadataMap[e].size},getRowStartIndexForOffset:function(t,e,o){return x("row",t,o,e)},getRowStopIndexForStartIndex:function(t,e,o,r){for(var n=t.rowCount,i=t.height,a=M("row",t,e,r),l=o+i,s=a.offset+a.size,c=e;c<n-1&&s<l;)c++,s+=M("row",t,c,r).size;return c},initInstanceProps:function(t,e){var o=t,r={columnMetadataMap:{},estimatedColumnWidth:o.estimatedColumnWidth||50,estimatedRowHeight:o.estimatedRowHeight||50,lastMeasuredColumnIndex:-1,lastMeasuredRowIndex:-1,rowMetadataMap:{}};return e.resetAfterColumnIndex=function(t,o){void 0===o&&(o=!0),e.resetAfterIndices({columnIndex:t,shouldForceUpdate:o})},e.resetAfterRowIndex=function(t,o){void 0===o&&(o=!0),e.resetAfterIndices({rowIndex:t,shouldForceUpdate:o})},e.resetAfterIndices=function(t){var o=t.columnIndex,n=t.rowIndex,i=t.shouldForceUpdate,a=void 0===i||i;"number"===typeof o&&(r.lastMeasuredColumnIndex=Math.min(r.lastMeasuredColumnIndex,o-1)),"number"===typeof n&&(r.lastMeasuredRowIndex=Math.min(r.lastMeasuredRowIndex,n-1)),e._getItemStyleCache(-1),a&&e.forceUpdate()},r},shouldResetStyleCacheOnItemSizeChange:!1,validateProps:function(t){t.columnWidth,t.rowHeight}}),T=function(t,e){return t};function z(t){var e,o,r=t.getItemOffset,c=t.getEstimatedTotalSize,u=t.getItemSize,h=t.getOffsetForIndexAndAlignment,m=t.getStartIndexForOffset,g=t.getStopIndexForStartIndex,v=t.initInstanceProps,S=t.shouldResetStyleCacheOnItemSizeChange,I=t.validateProps;return o=e=function(t){function e(e){var o;return(o=t.call(this,e)||this)._instanceProps=v(o.props,a(a(o))),o._outerRef=void 0,o._resetIsScrollingTimeoutId=null,o.state={instance:a(a(o)),isScrolling:!1,scrollDirection:"forward",scrollOffset:"number"===typeof o.props.initialScrollOffset?o.props.initialScrollOffset:0,scrollUpdateWasRequested:!1},o._callOnItemsRendered=void 0,o._callOnItemsRendered=l((function(t,e,r,n){return o.props.onItemsRendered({overscanStartIndex:t,overscanStopIndex:e,visibleStartIndex:r,visibleStopIndex:n})})),o._callOnScroll=void 0,o._callOnScroll=l((function(t,e,r){return o.props.onScroll({scrollDirection:t,scrollOffset:e,scrollUpdateWasRequested:r})})),o._getItemStyle=void 0,o._getItemStyle=function(t){var e,n=o.props,i=n.direction,a=n.itemSize,l=n.layout,s=o._getItemStyleCache(S&&a,S&&l,S&&i);if(s.hasOwnProperty(t))e=s[t];else{var c=r(o.props,t,o._instanceProps),d=u(o.props,t,o._instanceProps),f="horizontal"===i||"horizontal"===l,h="rtl"===i,m=f?c:0;s[t]=e={position:"absolute",left:h?void 0:m,right:h?m:void 0,top:f?0:c,height:f?"100%":d,width:f?d:"100%"}}return e},o._getItemStyleCache=void 0,o._getItemStyleCache=l((function(t,e,o){return{}})),o._onScrollHorizontal=function(t){var e=t.currentTarget,r=e.clientWidth,n=e.scrollLeft,i=e.scrollWidth;o.setState((function(t){if(t.scrollOffset===n)return null;var e=o.props.direction,a=n;if("rtl"===e)switch(p()){case"negative":a=-n;break;case"positive-descending":a=i-r-n}return a=Math.max(0,Math.min(a,i-r)),{isScrolling:!0,scrollDirection:t.scrollOffset<n?"forward":"backward",scrollOffset:a,scrollUpdateWasRequested:!1}}),o._resetIsScrollingDebounced)},o._onScrollVertical=function(t){var e=t.currentTarget,r=e.clientHeight,n=e.scrollHeight,i=e.scrollTop;o.setState((function(t){if(t.scrollOffset===i)return null;var e=Math.max(0,Math.min(i,n-r));return{isScrolling:!0,scrollDirection:t.scrollOffset<e?"forward":"backward",scrollOffset:e,scrollUpdateWasRequested:!1}}),o._resetIsScrollingDebounced)},o._outerRefSetter=function(t){var e=o.props.outerRef;o._outerRef=t,"function"===typeof e?e(t):null!=e&&"object"===typeof e&&e.hasOwnProperty("current")&&(e.current=t)},o._resetIsScrollingDebounced=function(){null!==o._resetIsScrollingTimeoutId&&d(o._resetIsScrollingTimeoutId),o._resetIsScrollingTimeoutId=f(o._resetIsScrolling,150)},o._resetIsScrolling=function(){o._resetIsScrollingTimeoutId=null,o.setState({isScrolling:!1},(function(){o._getItemStyleCache(-1,null)}))},o}i(e,t),e.getDerivedStateFromProps=function(t,e){return O(t,e),I(t),null};var o=e.prototype;return o.scrollTo=function(t){t=Math.max(0,t),this.setState((function(e){return e.scrollOffset===t?null:{scrollDirection:e.scrollOffset<t?"forward":"backward",scrollOffset:t,scrollUpdateWasRequested:!0}}),this._resetIsScrollingDebounced)},o.scrollToItem=function(t,e){void 0===e&&(e="auto");var o=this.props.itemCount,r=this.state.scrollOffset;t=Math.max(0,Math.min(t,o-1)),this.scrollTo(h(this.props,t,e,r,this._instanceProps))},o.componentDidMount=function(){var t=this.props,e=t.direction,o=t.initialScrollOffset,r=t.layout;if("number"===typeof o&&null!=this._outerRef){var n=this._outerRef;"horizontal"===e||"horizontal"===r?n.scrollLeft=o:n.scrollTop=o}this._callPropsCallbacks()},o.componentDidUpdate=function(){var t=this.props,e=t.direction,o=t.layout,r=this.state,n=r.scrollOffset;if(r.scrollUpdateWasRequested&&null!=this._outerRef){var i=this._outerRef;if("horizontal"===e||"horizontal"===o)if("rtl"===e)switch(p()){case"negative":i.scrollLeft=-n;break;case"positive-ascending":i.scrollLeft=n;break;default:var a=i.clientWidth,l=i.scrollWidth;i.scrollLeft=l-a-n}else i.scrollLeft=n;else i.scrollTop=n}this._callPropsCallbacks()},o.componentWillUnmount=function(){null!==this._resetIsScrollingTimeoutId&&d(this._resetIsScrollingTimeoutId)},o.render=function(){var t=this.props,e=t.children,o=t.className,r=t.direction,i=t.height,a=t.innerRef,l=t.innerElementType,u=t.innerTagName,d=t.itemCount,f=t.itemData,h=t.itemKey,m=void 0===h?T:h,p=t.layout,g=t.outerElementType,v=t.outerTagName,S=t.style,I=t.useIsScrolling,w=t.width,M=this.state.isScrolling,x="horizontal"===r||"horizontal"===p,C=x?this._onScrollHorizontal:this._onScrollVertical,_=this._getRangeToRender(),R=_[0],y=_[1],z=[];if(d>0)for(var O=R;O<=y;O++)z.push(s.createElement(e,{data:f,key:m(O,f),index:O,isScrolling:I?M:void 0,style:this._getItemStyle(O)}));var b=c(this.props,this._instanceProps);return s.createElement(g||v||"div",{className:o,onScroll:C,ref:this._outerRefSetter,style:n({position:"relative",height:i,width:w,overflow:"auto",WebkitOverflowScrolling:"touch",willChange:"transform",direction:r},S)},s.createElement(l||u||"div",{children:z,ref:a,style:{height:x?"100%":b,pointerEvents:M?"none":void 0,width:x?b:"100%"}}))},o._callPropsCallbacks=function(){if("function"===typeof this.props.onItemsRendered&&this.props.itemCount>0){var t=this._getRangeToRender(),e=t[0],o=t[1],r=t[2],n=t[3];this._callOnItemsRendered(e,o,r,n)}if("function"===typeof this.props.onScroll){var i=this.state,a=i.scrollDirection,l=i.scrollOffset,s=i.scrollUpdateWasRequested;this._callOnScroll(a,l,s)}},o._getRangeToRender=function(){var t=this.props,e=t.itemCount,o=t.overscanCount,r=this.state,n=r.isScrolling,i=r.scrollDirection,a=r.scrollOffset;if(0===e)return[0,0,0,0];var l=m(this.props,a,this._instanceProps),s=g(this.props,l,a,this._instanceProps),c=n&&"backward"!==i?1:Math.max(1,o),u=n&&"forward"!==i?1:Math.max(1,o);return[Math.max(0,l-c),Math.max(0,Math.min(e-1,s+u)),l,s]},e}(s.PureComponent),e.defaultProps={direction:"ltr",itemData:void 0,layout:"vertical",overscanCount:2,useIsScrolling:!1},o}var O=function(t,e){t.children,t.direction,t.height,t.layout,t.innerTagName,t.outerTagName,t.width,e.instance},b=function(t,e,o){var r=t.itemSize,n=o.itemMetadataMap,i=o.lastMeasuredIndex;if(e>i){var a=0;if(i>=0){var l=n[i];a=l.offset+l.size}for(var s=i+1;s<=e;s++){var c=r(s);n[s]={offset:a,size:c},a+=c}o.lastMeasuredIndex=e}return n[e]},P=function(t,e,o,r,n){for(;r<=o;){var i=r+Math.floor((o-r)/2),a=b(t,i,e).offset;if(a===n)return i;a<n?r=i+1:a>n&&(o=i-1)}return r>0?r-1:0},W=function(t,e,o,r){for(var n=t.itemCount,i=1;o<n&&b(t,o,e).offset<r;)o+=i,i*=2;return P(t,e,Math.min(o,n-1),Math.floor(o/2),r)},D=function(t,e){var o=t.itemCount,r=e.itemMetadataMap,n=e.estimatedItemSize,i=e.lastMeasuredIndex,a=0;if(i>=o&&(i=o-1),i>=0){var l=r[i];a=l.offset+l.size}return a+(o-i-1)*n},F=z({getItemOffset:function(t,e,o){return b(t,e,o).offset},getItemSize:function(t,e,o){return o.itemMetadataMap[e].size},getEstimatedTotalSize:D,getOffsetForIndexAndAlignment:function(t,e,o,r,n){var i=t.direction,a=t.height,l=t.layout,s=t.width,c="horizontal"===i||"horizontal"===l?s:a,u=b(t,e,n),d=D(t,n),f=Math.max(0,Math.min(d-c,u.offset)),h=Math.max(0,u.offset-c+u.size);switch("smart"===o&&(o=r>=h-c&&r<=f+c?"auto":"center"),o){case"start":return f;case"end":return h;case"center":return Math.round(h+(f-h)/2);case"auto":default:return r>=h&&r<=f?r:r<h?h:f}},getStartIndexForOffset:function(t,e,o){return function(t,e,o){var r=e.itemMetadataMap,n=e.lastMeasuredIndex;return(n>0?r[n].offset:0)>=o?P(t,e,n,0,o):W(t,e,Math.max(0,n),o)}(t,o,e)},getStopIndexForStartIndex:function(t,e,o,r){for(var n=t.direction,i=t.height,a=t.itemCount,l=t.layout,s=t.width,c="horizontal"===n||"horizontal"===l?s:i,u=b(t,e,r),d=o+c,f=u.offset+u.size,h=e;h<a-1&&f<d;)h++,f+=b(t,h,r).size;return h},initInstanceProps:function(t,e){var o={itemMetadataMap:{},estimatedItemSize:t.estimatedItemSize||50,lastMeasuredIndex:-1};return e.resetAfterIndex=function(t,r){void 0===r&&(r=!0),o.lastMeasuredIndex=Math.min(o.lastMeasuredIndex,t-1),e._getItemStyleCache(-1),r&&e.forceUpdate()},o},shouldResetStyleCacheOnItemSizeChange:!1,validateProps:function(t){t.itemSize}}),L=v({getColumnOffset:function(t,e){return e*t.columnWidth},getColumnWidth:function(t,e){return t.columnWidth},getRowOffset:function(t,e){return e*t.rowHeight},getRowHeight:function(t,e){return t.rowHeight},getEstimatedTotalHeight:function(t){var e=t.rowCount;return t.rowHeight*e},getEstimatedTotalWidth:function(t){var e=t.columnCount;return t.columnWidth*e},getOffsetForColumnAndAlignment:function(t,e,o,r,n,i){var a=t.columnCount,l=t.columnWidth,s=t.width,c=Math.max(0,a*l-s),u=Math.min(c,e*l),d=Math.max(0,e*l-s+i+l);switch("smart"===o&&(o=r>=d-s&&r<=u+s?"auto":"center"),o){case"start":return u;case"end":return d;case"center":var f=Math.round(d+(u-d)/2);return f<Math.ceil(s/2)?0:f>c+Math.floor(s/2)?c:f;case"auto":default:return r>=d&&r<=u?r:d>u||r<d?d:u}},getOffsetForRowAndAlignment:function(t,e,o,r,n,i){var a=t.rowHeight,l=t.height,s=t.rowCount,c=Math.max(0,s*a-l),u=Math.min(c,e*a),d=Math.max(0,e*a-l+i+a);switch("smart"===o&&(o=r>=d-l&&r<=u+l?"auto":"center"),o){case"start":return u;case"end":return d;case"center":var f=Math.round(d+(u-d)/2);return f<Math.ceil(l/2)?0:f>c+Math.floor(l/2)?c:f;case"auto":default:return r>=d&&r<=u?r:d>u||r<d?d:u}},getColumnStartIndexForOffset:function(t,e){var o=t.columnWidth,r=t.columnCount;return Math.max(0,Math.min(r-1,Math.floor(e/o)))},getColumnStopIndexForStartIndex:function(t,e,o){var r=t.columnWidth,n=t.columnCount,i=t.width,a=e*r,l=Math.ceil((i+o-a)/r);return Math.max(0,Math.min(n-1,e+l-1))},getRowStartIndexForOffset:function(t,e){var o=t.rowHeight,r=t.rowCount;return Math.max(0,Math.min(r-1,Math.floor(e/o)))},getRowStopIndexForStartIndex:function(t,e,o){var r=t.rowHeight,n=t.rowCount,i=t.height,a=e*r,l=Math.ceil((i+o-a)/r);return Math.max(0,Math.min(n-1,e+l-1))},initInstanceProps:function(t){},shouldResetStyleCacheOnItemSizeChange:!0,validateProps:function(t){t.columnWidth,t.rowHeight}}),k=z({getItemOffset:function(t,e){return e*t.itemSize},getItemSize:function(t,e){return t.itemSize},getEstimatedTotalSize:function(t){var e=t.itemCount;return t.itemSize*e},getOffsetForIndexAndAlignment:function(t,e,o,r){var n=t.direction,i=t.height,a=t.itemCount,l=t.itemSize,s=t.layout,c=t.width,u="horizontal"===n||"horizontal"===s?c:i,d=Math.max(0,a*l-u),f=Math.min(d,e*l),h=Math.max(0,e*l-u+l);switch("smart"===o&&(o=r>=h-u&&r<=f+u?"auto":"center"),o){case"start":return f;case"end":return h;case"center":var m=Math.round(h+(f-h)/2);return m<Math.ceil(u/2)?0:m>d+Math.floor(u/2)?d:m;case"auto":default:return r>=h&&r<=f?r:r<h?h:f}},getStartIndexForOffset:function(t,e){var o=t.itemCount,r=t.itemSize;return Math.max(0,Math.min(o-1,Math.floor(e/r)))},getStopIndexForStartIndex:function(t,e,o){var r=t.direction,n=t.height,i=t.itemCount,a=t.itemSize,l=t.layout,s=t.width,c=e*a,u="horizontal"===r||"horizontal"===l?s:n,d=Math.ceil((u+o-c)/a);return Math.max(0,Math.min(i-1,e+d-1))},initInstanceProps:function(t){},shouldResetStyleCacheOnItemSizeChange:!0,validateProps:function(t){t.itemSize}});function H(t,e){for(var o in t)if(!(o in e))return!0;for(var r in e)if(t[r]!==e[r])return!0;return!1}function A(t,e){var o=t.style,r=c(t,["style"]),n=e.style,i=c(e,["style"]);return!H(o,n)&&!H(r,i)}e.VariableSizeGrid=y,e.VariableSizeList=F,e.FixedSizeGrid=L,e.FixedSizeList=k,e.areEqual=A,e.shouldComponentUpdate=function(t,e){return!A(this.props,t)||H(this.state,e)}},2464:function(t,e,o){"use strict";function r(t,e){if(t.length!==e.length)return!1;for(var o=0;o<t.length;o++)if(t[o]!==e[o])return!1;return!0}t.exports=function(t,e){var o;void 0===e&&(e=r);var n,i=[],a=!1;return function(){for(var r=[],l=0;l<arguments.length;l++)r[l]=arguments[l];return a&&o===this&&e(r,i)||(n=t.apply(this,r),a=!0,o=this,i=r),n}}}}]);
//# sourceMappingURL=5.a7ee0c30.chunk.js.map