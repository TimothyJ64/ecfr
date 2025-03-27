import React, { useEffect, useState } from "react";
import { Button } from "./components/ui/button";
import { ScrollArea } from "./components/ui/scroll-area";

function TreeNode({ node, level = 0, expandedNodes, toggleNode }) {
  const isOpen = expandedNodes[node.fullPath] || false;
  const hasChildren = node.children && node.children.length > 0;

  return (
    <div style={{ marginLeft: `${level * 1.25}rem` }} className="mb-1">
      <div
        className="cursor-pointer hover:underline text-sm text-slate-300"
        onClick={() => toggleNode(node.fullPath)}
      >
        {hasChildren && (
          <span className="mr-1 text-cyan-400">{isOpen ? "▼" : "▶"}</span>
        )}
        {node.label}
      </div>
      {isOpen && hasChildren && (
        <div className="mt-1">
          {node.children.map((child, idx) => (
            <TreeNode
              key={child.fullPath}
              node={child}
              level={level + 1}
              expandedNodes={expandedNodes}
              toggleNode={toggleNode}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function buildTree(agency) {
  const tree = [];
  const makeNode = (label, path, children = []) => ({
    label,
    fullPath: path,
    children,
  });

  const titles = agency.parts_by_reference || [];
  titles.forEach((titleRef) => {
    const titlePath = `${agency.agency} > Title ${titleRef.title}`;
    const titleNode = makeNode(`📘 Title ${titleRef.title}`, titlePath);

    const chapterLabel = titleRef.chapter || "Unknown Chapter";
    const chapterPath = `${titlePath} > ${chapterLabel}`;
    const chapterNode = makeNode(chapterLabel, chapterPath);

    chapterNode.children = (titleRef.parts_by_subchapter || []).map((sub) => {
      const subPath = `${chapterPath} > ${sub.subchapter}`;
      return makeNode(sub.subchapter, subPath,
        (sub.parts || []).map((part) => {
          const partPath = `${subPath} > ${part.part}`;
          return makeNode(part.part, partPath,
            (part.sections || []).map((sec) => {
              return makeNode(sec, `${partPath} > ${sec}`);
            })
          );
        })
      );
    });

    titleNode.children = [chapterNode];
    tree.push(titleNode);
  });

  if (agency.metrics) {
    const mPath = `${agency.agency} > 📊 Metrics`;
    const metricNode = makeNode("📊 Metrics", mPath, [
      makeNode(`Titles: ${agency.metrics.title_count}`, `${mPath} > Titles`),
      makeNode(`Chapters: ${agency.metrics.chapter_count}`, `${mPath} > Chapters`),
      makeNode(`Subchapters: ${agency.metrics.subchapter_count}`, `${mPath} > Subchapters`),
      makeNode(`Parts: ${agency.metrics.part_count}`, `${mPath} > Parts`),
      makeNode(`Sections: ${agency.metrics.section_count}`, `${mPath} > Sections`)
    ]);

    const changeHistory = agency.change_history;
    if (changeHistory?.items?.length) {
      const changeItems = changeHistory.items.map((item) => {
        const itemLabel = `${item.date}: ${item.item}`;
        const itemPath = `${mPath} > Change History > ${itemLabel}`;
        return makeNode(itemLabel, itemPath, [
          makeNode(item.path || "No path", `${itemPath} > path`)
        ]);
      }); 
     tree.push(makeNode(`📜 Change History: ${changeHistory.range}`, `${mPath} > Change History`, changeItems))
    }

    tree.push(metricNode); 
  }

  return tree;
}

export default function ECFRDashboard() {
  const [agencies, setAgencies] = useState([]);
  const [expandedAgencies, setExpandedAgencies] = useState({});
  const [expandedNodes, setExpandedNodes] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("/api/agencies/history");
        const json = await res.json();
        if (json?.data) setAgencies(json.data);
        else throw new Error("No data returned in response.");
      } catch (err) {
        console.error("Failed to load agency history", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  const toggleAgency = (slug) => {
    setExpandedAgencies((prev) => ({ ...prev, [slug]: !prev[slug] }));
  };

  const toggleNode = (path) => {
    setExpandedNodes((prev) => ({ ...prev, [path]: !prev[path] }));
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6">
      <header className="sticky top-0 z-10 bg-slate-900 pb-4">
        <h1 className="text-4xl font-extrabold text-center mb-2">
          eCFR Agency Rule Explorer
        </h1>
      </header>
      {loading ? (
        <p className="text-center mt-8">Loading agency history...</p>
      ) : error ? (
        <p className="text-red-400 text-center mt-8">Error: {error}</p>
      ) : (
        <ScrollArea className="h-[calc(100vh-8rem)] pr-2">
          <div className="text-left text-white space-y-6">
            {agencies.map((agency, idx) => (
              <div key={idx} className="border-l-2 border-cyan-700 pl-4">
                <div
                  className="cursor-pointer text-cyan-300 font-semibold text-lg"
                  onClick={() => toggleAgency(agency.slug)}
                >
                  {expandedAgencies[agency.slug] ? "▼" : "▶"} {agency.agency}
                </div>
                {expandedAgencies[agency.slug] && (
                  <div className="ml-4 mt-2">
                    {buildTree(agency).map((node) => (
                      <TreeNode
                        key={node.fullPath}
                        node={node}
                        expandedNodes={expandedNodes}
                        toggleNode={toggleNode}
                      />
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </ScrollArea>
      )}
    </div>
  );
}
