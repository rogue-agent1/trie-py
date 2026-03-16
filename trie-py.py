#!/usr/bin/env python3
"""Trie data structure for prefix search and autocomplete."""
import json, argparse, os, sys
class Trie:
    def __init__(self): self.root = {}
    def insert(self, word):
        node = self.root
        for c in word: node = node.setdefault(c, {})
        node["$"] = True
    def search(self, word):
        node = self.root
        for c in word:
            if c not in node: return False
            node = node[c]
        return "$" in node
    def starts_with(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node: return []
            node = node[c]
        results = []
        def collect(n, p):
            if "$" in n: results.append(p)
            for c, child in n.items():
                if c != "$": collect(child, p + c)
        collect(node, prefix)
        return results
    def to_dict(self): return self.root
    @classmethod
    def from_dict(cls, d): t = cls(); t.root = d; return t
def main():
    p = argparse.ArgumentParser(); p.add_argument("--db", default="trie.json")
    sub = p.add_subparsers(dest="cmd")
    a = sub.add_parser("add"); a.add_argument("words", nargs="+")
    a = sub.add_parser("search"); a.add_argument("word")
    a = sub.add_parser("prefix"); a.add_argument("prefix"); a.add_argument("-n", type=int, default=10)
    a = sub.add_parser("load"); a.add_argument("file")
    args = p.parse_args()
    t = Trie.from_dict(json.load(open(args.db))) if os.path.exists(args.db) else Trie()
    if args.cmd == "add":
        for w in args.words: t.insert(w)
        json.dump(t.to_dict(), open(args.db, "w")); print(f"Added {len(args.words)}")
    elif args.cmd == "search": print("found" if t.search(args.word) else "not found")
    elif args.cmd == "prefix":
        for w in t.starts_with(args.prefix)[:args.n]: print(w)
    elif args.cmd == "load":
        for line in open(args.file): t.insert(line.strip())
        json.dump(t.to_dict(), open(args.db, "w")); print("Loaded")
if __name__ == "__main__": main()
