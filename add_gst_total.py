import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_modal = """    <div style="padding:24px">
      <div class="fg"><label>Price (&#8377; per page/item)</label><input type="number" id="fpPrice" step="0.01" min="0" placeholder="0.00" style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem"></div>
      <button class="btn-sm btn-orange" onclick="saveFeaturePrice()" style="width:100%;margin-top:16px;padding:12px">Save Price</button>
    </div>"""

new_modal = """    <div style="padding:24px">
      <div class="fg"><label>Price (&#8377;)</label><input type="text" inputmode="decimal" id="fpPrice" placeholder="0.00" oninput="recalcFeatureTotal()" style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem"></div>
      <div class="fg" style="margin-top:12px"><label>GST (%)</label><input type="text" inputmode="decimal" id="fpGst" placeholder="0" oninput="recalcFeatureTotal()" style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem"></div>
      <div class="fg" style="margin-top:12px"><label>Total Cost (&#8377;)</label><input type="text" id="fpTotal" readonly style="width:100%;padding:12px 14px;border:1.5px solid #e0e0e0;border-radius:10px;font-size:.9rem;background:#f7f7f7;font-weight:700"></div>
      <button class="btn-sm btn-orange" onclick="saveFeaturePrice()" style="width:100%;margin-top:16px;padding:12px">Save Price</button>
    </div>"""

if old_modal not in content:
    print("MODAL FIELDS NOT FOUND - aborting")
else:
    content = content.replace(old_modal, new_modal, 1)

    old_open = """  document.getElementById('fpPrice').value='';
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
}"""

    new_open = """  document.getElementById('fpPrice').value='';
  document.getElementById('fpGst').value='';
  document.getElementById('fpTotal').value='';
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
  recalcFeatureTotal();
}
function recalcFeatureTotal(){
  const price=parseFloat(document.getElementById('fpPrice').value)||0;
  const gst=parseFloat(document.getElementById('fpGst').value)||0;
  const total=price+(price*gst/100);
  document.getElementById('fpTotal').value=total.toFixed(2);
}"""

    if old_open not in content:
        print("OPEN FUNCTION NOT FOUND - aborting (modal fields already patched though)")
    else:
        content = content.replace(old_open, new_open, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
