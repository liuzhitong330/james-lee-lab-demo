(function () {
  'use strict';
  const data = window.LEE_DATA;
  const $ = id => document.getElementById(id);
  const names = {PD1:'PD-1',CTLA4:'CTLA-4',ICOS:'ICOS',IFNg:'IFNγ','Tetramer abundance':'Tetramer+ abundance'};
  const number = v => (v > 0 ? '+' : '') + v.toFixed(1);
  const result = (m,c) => data.results.find(r => r.marker === m && r.contrast === c);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const ns = 'http://www.w3.org/2000/svg';
  function node(tag,attrs={},text='') {const n=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));if(text)n.textContent=text;return n;}
  function eligible(m) {
    const t=+$('threshold').value, robust=$('robust').checked;
    return data.contrasts.every(c => {const r=result(m,c.id);const score=c.expected<0 ? -(robust?r.loo_max:r.delta) : (robust?r.loo_min:r.delta);return score>=t;});
  }
  function selectedCandidates() {return data.markers.slice(0,4).filter(eligible);}
  function draw(svg,r,c,abundance=false) {
    svg.replaceChildren();
    const height=abundance?260:285, top=30, bottom=height-60, y=v=>bottom-(v/100)*(bottom-top), xs=[195,430];
    svg.append(node('title',{},`${names[r.marker]}: ${c.a_label} mean ${r.mean_a.toFixed(2)}%, ${c.b_label} mean ${r.mean_b.toFixed(2)}%.`));
    svg.append(node('text',{x:12,y:15,class:'axis-label'},abundance?'% of CD8+ cells':'% of KSP-tetramer+ CD8+ cells'));
    [0,25,50,75,100].forEach(v=>{svg.append(node('line',{x1:57,x2:574,y1:y(v),y2:y(v),stroke:'#e5e5e5'}));svg.append(node('text',{x:45,y:y(v)+4,'text-anchor':'end',class:'axis-label'},String(v)));});
    [['a',c.a_label],['b',c.b_label]].forEach(([group,label],gi)=>{
      const records=r.groups[group], x=xs[gi], color=gi?'#1f7a8c':'#777';
      records.forEach((d,i)=>{const offset=((i*7)%records.length-(records.length-1)/2)*3.2;const dot=node('circle',{cx:x+offset,cy:y(d.value),r:4.3,fill:color,'fill-opacity':.72});dot.append(node('title',{},`${label}: ${d.value}% · ${d.source_sheet}!${d.source_cell}`));svg.append(dot);});
      const mean=gi?r.mean_b:r.mean_a;svg.append(node('line',{x1:x-35,x2:x+35,y1:y(mean),y2:y(mean),stroke:'#1a1a1a','stroke-width':2}));
      svg.append(node('text',{x,y:bottom+25,'text-anchor':'middle',class:'group-label'},label));
      svg.append(node('text',{x,y:bottom+44,'text-anchor':'middle',class:'axis-label'},`n=${records.length} · mean ${mean.toFixed(1)}%`));
    });
  }
  function planRows() {
    const candidates=selectedCandidates();
    return [{endpoint:'KSP-tetramer+ abundance',parent:'CD8+ T cells',measurement:'Phenotyping; record preparation / stimulation state'},...candidates.map(m=>({endpoint:names[m]+' positive',parent:'KSP-tetramer+ CD8+ T cells',measurement:m==='IFNg'?'Stimulated intracellular cytokine; record stimulation and matched control':'Phenotyping; record preparation / stimulation state'}))];
  }
  function render() {
    const selected=$('marker').value, c=data.contrasts.find(x=>x.id===$('contrast').value), r=result(selected,c.id), shortlisted=selectedCandidates();
    $('shortlist').innerHTML=`<strong>Provisional shortlist: ${shortlisted.length?shortlisted.map(x=>names[x]).join(' + '):'none at this setting'}.</strong> ${$('robust').checked?'Every single-observation omission must still meet':'Each full-data mean difference must meet'} the ${$('threshold').value}-point directional cutoff in all four contrasts. This is a filter for discussion, not a validated panel.`;
    const table=$('effect-table');
    table.innerHTML='<caption>Mean differences, percentage points. Liver: SQ + liver minus SQ only. Other columns: intervention minus its own control.</caption><thead><tr><th scope="col">Readout</th>'+data.contrasts.map(x=>`<th scope="col">${esc(x.short)}<br><span class="expect">${x.expected<0?'decrease ↓':'increase ↑'}</span></th>`).join('')+'</tr></thead><tbody>'+data.markers.slice(0,4).map(m=>`<tr class="${m===selected?'selected-row':''}"><th scope="row"><button type="button" data-marker="${m}" aria-pressed="${m===selected}">${names[m]}</button><span class="status">${eligible(m)?'candidate':'outside rule'}</span></th>`+data.contrasts.map(c=>`<td>${number(result(m,c.id).delta)}</td>`).join('')+'</tr>').join('')+'</tbody>';
    table.querySelectorAll('button[data-marker]').forEach(b=>b.addEventListener('click',()=>{$('marker').value=b.dataset.marker;render();}));
    $('chart-heading').textContent=names[selected]+' · '+c.label;
    draw($('hero-viz'),r,c);
    $('readout').innerHTML=`Mean change: <strong>${number(r.delta)} percentage points</strong>. Median change: ${number(r.median_delta)}. Single-observation omission range: ${number(r.loo_min)} to ${number(r.loo_max)} points (not a confidence interval).`;
    $('point-caption').textContent=c.description+' Dots are published endpoint observations; black lines are group means. Values are not paired. Hover for source cells, or open the accessible table below.';
    $('source-values').innerHTML='<p>Δ = mean(second group) − mean(first group). For each omission, recompute Δ after removing one value from one group only; report the smallest and largest result.</p><table><thead><tr><th>Group</th><th>Value (%)</th><th>Workbook cell</th></tr></thead><tbody>'+[...r.groups.a,...r.groups.b].map(x=>`<tr><td>${esc(x.group)}</td><td>${x.value}</td><td>${esc(x.source_sheet)}!${x.source_cell}</td></tr>`).join('')+'</tbody></table>';
    $('metric-one').textContent=shortlisted.length+' / 4';
    const abundance=result('Tetramer abundance',c.id);draw($('abundance-viz'),abundance,c,true);
    $('abundance-note').textContent=`Abundance difference: ${number(abundance.delta)} percentage points (${abundance.groups.a[0].source_sheet}). This distinct denominator is retained as context, not subjected to the state-marker rule. A small difference is not evidence of equivalence.`;
    $('plan').innerHTML='<ul>'+planRows().map(x=>`<li><strong>${esc(x.endpoint)}</strong> / ${esc(x.parent)}<br><span>${esc(x.measurement)}</span></li>`).join('')+'</ul>';
  }
  ['threshold','robust','marker','contrast'].forEach(id=>$(id).addEventListener('change',render));
  $('download-plan').addEventListener('click',()=>{
    const columns=['record_type','animal_id','specimen_id','tissue_site','aliquot_id','processing_batch','endpoint','parent_population','value_percent','stimulation_record','acquisition_version','gating_version','qc_exclusion_reason','selection_cutoff_pp','selection_uses_omission_check'];
    const rows=planRows().map(x=>['PROSPECTIVE_TEMPLATE','','','','','',x.endpoint,x.parent,'',x.measurement,'','','',$('threshold').value,String($('robust').checked)]);
    const csv=[columns,...rows].map(r=>r.map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(',')).join('\r\n');
    const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='prospective-specimen-readouts.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  render();
})();
