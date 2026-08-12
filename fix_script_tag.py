import io

path = r"static\specific_control.html"
with io.open(path, "r", encoding="utf-8") as f:
    content = f.read()

old = """    if(btn){btn.disabled=false;btn.textContent='Raise Ticket';}
  }
}
<!-- OUT FOR DELIVERY PICKER MODAL -->"""

new = """    if(btn){btn.disabled=false;btn.textContent='Raise Ticket';}
  }
}
</script>
<!-- OUT FOR DELIVERY PICKER MODAL -->"""

if old not in content:
    print("OLD BLOCK NOT FOUND - aborting")
else:
    content = content.replace(old, new, 1)
    # Remove the now-redundant trailing </script> right before </body>
    old2 = "</script>\n</body>\n</html>"
    new2 = "</body>\n</html>"
    if old2 in content:
        content = content.replace(old2, new2, 1)
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("PATCHED SUCCESSFULLY")
    else:
        print("TRAILING SCRIPT TAG PATTERN NOT FOUND - manual check needed")
