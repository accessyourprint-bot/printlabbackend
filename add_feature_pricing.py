import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add price modal HTML right after the App Control panel
old_anchor = """<div id="fcFeatureList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px"></div>
</div>"""

new_anchor = """<div id="fcFeatureList" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px"></div>
</div>

<div id="fpMo" class="mo hidden">
  <div class="mb">
    <div class="mh">
      <div><h3 id="fpTitle">Feature Price</h3><p>Set the price for this feature.</p></div>
      <button class="mx" onclick="cMo('fpMo')">&#10005;</button>
    </div>
    <div class="mbody">
      <div class="fg"><label>Price (&#8377; per page/item)</label><input type="number" id="fpPrice" step="0.01" min="0" placeholder="0.00" style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem"></div>
    </div>
    <div class="mfoot"><button class="bsb" onclick="saveFeaturePrice()" style="width:100%">Save Price</button></div>
  </div>
</div>"""

if old_anchor not in content:
    print("ANCHOR NOT FOUND - aborting")
else:
    content = content.replace(old_anchor, new_anchor, 1)

    # 2. Update the render function: name click opens price modal, switch stays independently clickable
    old_render = """  list.innerHTML=flags.map(f=>
    '<label style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border:1px solid #ececf1;border-radius:10px;cursor:pointer;background:'+(f.enabled?'#fff':'#faf7f5')+'">'+
    '<span style="font-size:.86rem;font-weight:600;color:'+(f.enabled?'#1a223e':'#aaa')+'">'+f.label+'</span>'+
    '<span class="switch"><input type="checkbox" '+(f.enabled?'checked':'')+' onchange="toggleFeatureFlag(\\''+f.feature_name+'\\', this.checked)"><span class="slider"></span></span>'+
    '</label>'
  ).join('');
}"""

    new_render = """  list.innerHTML=flags.map(f=>
    '<div style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;border:1px solid #ececf1;border-radius:10px;background:'+(f.enabled?'#fff':'#faf7f5')+'">'+
    '<span style="font-size:.86rem;font-weight:600;color:'+(f.enabled?'#1a223e':'#aaa')+';cursor:pointer" onclick="openFeaturePrice(\\''+f.feature_name+'\\',\\''+f.label.replace(/"/g,'')+'\\')">'+f.label+'</span>'+
    '<label class="switch"><input type="checkbox" '+(f.enabled?'checked':'')+' onchange="toggleFeatureFlag(\\''+f.feature_name+'\\', this.checked)"><span class="slider"></span></label>'+
    '</div>'
  ).join('');
}
let curFeaturePricing=null;
async function openFeaturePrice(featureName,label){
  oMo('fpMo');
  document.getElementById('fpTitle').textContent=label+' - Price';
  document.getElementById('fpPrice').value='';
  curFeaturePricing=null;
  try{
    const list=await api('/api/v1/pricing');
    const items=Array.isArray(list)?list:[];
    const match=items.find(p=>p.print_type===featureName);
    if(match){
      curFeaturePricing={id:match.id,print_type:featureName};
      document.getElementById('fpPrice').value=match.price_per_page;
    }else{
      curFeaturePricing={id:null,print_type:featureName};
    }
  }catch(e){}
}
async function saveFeaturePrice(){
  const price=parseFloat(document.getElementById('fpPrice').value);
  if(isNaN(price)||price<0){alert('Enter a valid price');return;}
  if(!curFeaturePricing){alert('No feature selected');return;}
  try{
    if(curFeaturePricing.id){
      await fetch(API+'/api/v1/pricing/'+curFeaturePricing.id+'?price_per_page='+price,{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    }else{
      await api('/api/v1/pricing','POST',{print_type:curFeaturePricing.print_type,price_per_page:price,is_global:true});
    }
    cMo('fpMo');
    alert('Price saved');
  }catch(e){alert('Failed to save price');}
}"""

    if old_render not in content:
        print("RENDER FUNCTION NOT FOUND - aborting (modal HTML already added though)")
    else:
        content = content.replace(old_render, new_render, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
