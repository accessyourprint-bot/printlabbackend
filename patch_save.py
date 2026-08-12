import io

path = r"static\full_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_save = """async function saveFeaturePrice(){
  const price=parseFloat(document.getElementById('fpPrice').value);
  if(isNaN(price)||price<0){alert('Enter a valid price');return;}
  if(!curFeaturePricing){alert('No feature selected');return;}
  try{
    if(curFeaturePricing.id){
      await fetch(API+'/api/v1/pricing/'+curFeaturePricing.id+'?price_per_page='+price,{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    }else{
      await api('/api/v1/pricing','POST',{print_type:curFeaturePricing.print_type,price_per_page:price,is_global:true});
    }
    document.getElementById('fpMo').style.display='none';
    alert('Price saved');
  }catch(e){alert('Failed to save price');}
}"""

new_save = """async function saveFeaturePrice(){
  const price=parseFloat(document.getElementById('fpPrice').value);
  const gst=parseFloat(document.getElementById('fpGst').value)||0;
  if(isNaN(price)||price<0){alert('Enter a valid price');return;}
  if(!curFeaturePricing){alert('No feature selected');return;}
  try{
    if(curFeaturePricing.id){
      await fetch(API+'/api/v1/pricing/'+curFeaturePricing.id+'?price_per_page='+price+'&gst_percent='+gst,{method:'PATCH',headers:{'Authorization':'Bearer '+tok}});
    }else{
      await api('/api/v1/pricing','POST',{print_type:curFeaturePricing.print_type,price_per_page:price,gst_percent:gst,is_global:true});
    }
    document.getElementById('fpMo').style.display='none';
    alert('Price saved');
  }catch(e){alert('Failed to save price');}
}"""

if old_save not in content:
    print("SAVE FUNCTION NOT FOUND - aborting")
else:
    content = content.replace(old_save, new_save, 1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("PATCHED SUCCESSFULLY")
