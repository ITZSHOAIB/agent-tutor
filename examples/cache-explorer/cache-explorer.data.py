"""Measure the cache explorer data. usage: uv run --with transformers --with jinja2 python cache-explorer.data.py cache-explorer.data.json"""
import json, copy, sys
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct", local_files_only=False)
def fn(name, desc, props):
    return {"type":"function","function":{"name":name,"description":desc,"parameters":{"type":"object","properties":{k:{"type":"string"} for k in props},"required":list(props)}}}
TOOLS=[fn("read_file","Read a file from the repository.",["path"]), fn("run_tests","Run the test suite and return failures.",["pattern"])]
SYS="You are a coding agent working in the user's repository. Keep answers short."
MSGS=[
 {"role":"system","content":SYS},
 {"role":"user","content":"The login test fails. Can you look?"},
 {"role":"assistant","content":"","tool_calls":[{"type":"function","function":{"name":"run_tests","arguments":{"pattern":"login"}}}]},
 {"role":"tool","content":"FAILED test_login.py::test_expired_token - assert 401 == 200"},
 {"role":"assistant","content":"The expired-token case returns 401. The test expects 200, so the test is wrong, not the code."},
]
def render(msgs, tools):
    return tok.apply_chat_template(msgs, tools=tools, tokenize=False, add_generation_prompt=True)
def ids(s): return tok(s).input_ids
base = render(MSGS, TOOLS)
bids = ids(base)
# segments by character range in base text
segs=[]
def add(label, kind, start, end): segs.append(dict(label=label, kind=kind, start=start, end=end))
i = base.index("<|im_start|>system"); j = base.index("\n\n# Tools"); add("System prompt","system",0,j)
k = base.index("<|im_end|>", j); add("Tool definitions (inserted by the template)","tools",j,k+len("<|im_end|>\n"))
pos = k+len("<|im_end|>\n")
names={"user":"User message","assistant":"Assistant turn","tool":"Tool result"}
kinds=[]
for m in MSGS[1:]:
    e = base.index("<|im_end|>\n", pos)+len("<|im_end|>\n")
    lab = names[m["role"]]
    if m["role"]=="assistant" and m.get("tool_calls"): lab="Assistant tool call"
    add(lab, m["role"] if m["role"]!="tool" else "result", pos, e); pos=e
add("Generation marker","gen",pos,len(base))
# token offsets for char->token mapping
enc = tok(base, return_offsets_mapping=True); offs=enc["offset_mapping"]
def tok_at_char(c):
    for t,(a,b) in enumerate(offs):
        if b>c: return t
    return len(offs)
for s in segs: s["tokStart"]=tok_at_char(s["start"]); s["tokEnd"]=tok_at_char(s["end"])
def lcp(a,b):
    n=0
    for x,y in zip(a,b):
        if x!=y: break
        n+=1
    return n
def char_of_tok(t): return offs[t][0] if t<len(offs) else len(base)
V=[]
def variant(key,label,msgs,tools,what):
    s=render(msgs,tools); v=ids(s); n=lcp(bids,v)
    V.append(dict(key=key,label=label,what=what,shared=n,total=len(v),baseTotal=len(bids),newTokens=len(v)-n,sharedChar=char_of_tok(n),blocks16=(n//16)*16))
m=copy.deepcopy(MSGS); m.append({"role":"user","content":"Fix the test then."})
variant("append","Append a new user message",m,TOOLS,"The next turn of the same conversation.")
t=TOOLS+[fn("git_diff","Show uncommitted changes.",["path"])]
variant("tool","Add one tool",MSGS,t,"A third tool, git_diff, added to the end of the tools list.")
m=copy.deepcopy(MSGS); m[0]["content"]=SYS.replace("short","very short")
variant("system","Change one word in the system prompt",m,TOOLS,"\"short\" becomes \"very short\".")
m=copy.deepcopy(MSGS); m[3]["content"]=m[3]["content"].replace("401","403")
variant("result","Change the old tool result",m,TOOLS,"One digit in the tool result from four messages ago.")
out=dict(model="Qwen/Qwen2.5-0.5B-Instruct", text=base, tokens=len(bids), segments=segs, variants=V)
json.dump(out, open(sys.argv[1],"w",encoding="utf8"), ensure_ascii=False, indent=1)
for s in segs: print(s["label"], s["tokStart"], s["tokEnd"])
for v in V: print(v["key"], v["shared"], "/", v["total"], "blocks16", v["blocks16"])
