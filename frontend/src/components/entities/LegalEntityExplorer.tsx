import React from "react";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { CATEGORY_STYLES, EntityItem } from "./SmartEntityHighlighter";

interface EntityGroupItem {
  text: string;
  normalized?: string;
  label: string;
  confidence?: number;
  occurrences: Array<{ start: number; end: number; text: string }>;
}

interface LegalEntityExplorerProps {
  groupedEntities: Record<string, EntityGroupItem[]>;
  onSelectEntity: (entity: EntityItem) => void;
  selectedEntity: EntityItem | null;
}

const LegalEntityExplorer: React.FC<LegalEntityExplorerProps> = ({
  groupedEntities,
  onSelectEntity,
  selectedEntity,
}) => {
  const groups = Object.entries(groupedEntities || {});

  if (groups.length === 0) {
    return (
      <div className="p-6 text-center text-muted-foreground text-sm border rounded-xl bg-card">
        No entities extracted yet.
      </div>
    );
  }

  return (
    <div className="space-y-4 max-h-[550px] overflow-y-auto pr-1">
      {groups.map(([groupName, items]) => {
        if (!items || items.length === 0) return null;

        return (
          <div key={groupName} className="border border-border/60 rounded-xl p-3 bg-card/60 shadow-sm">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-xs font-semibold tracking-wide uppercase text-muted-foreground">
                {groupName}
              </h4>
              <Badge variant="secondary" className="text-[10px] h-5 px-1.5">
                {items.length}
              </Badge>
            </div>

            <div className="flex flex-wrap gap-1.5">
              {items.map((item, idx) => {
                const style = CATEGORY_STYLES[item.label] || {
                  bg: "bg-gray-100",
                  text: "text-gray-800",
                  border: "border-gray-300",
                };
                const isSelected = selectedEntity && selectedEntity.text === item.text;

                return (
                  <button
                    key={`${item.text}-${idx}`}
                    onClick={() => {
                      const firstOcc = item.occurrences[0] || { start: 0, end: item.text.length, text: item.text };
                      onSelectEntity({
                        text: item.text,
                        label: item.label,
                        normalized: item.normalized,
                        confidence: item.confidence,
                        start: firstOcc.start,
                        end: firstOcc.end,
                      });
                    }}
                    className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-xs border transition-all text-left ${
                      style.bg
                    } ${style.text} ${style.border} ${
                      isSelected ? "ring-2 ring-primary ring-offset-1 font-semibold" : "hover:brightness-95"
                    }`}
                  >
                    <span className="truncate max-w-[180px]">{item.text}</span>
                    <span className="text-[9px] bg-white/70 px-1 py-0.2 rounded-full font-bold">
                      {item.occurrences.length}x
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default LegalEntityExplorer;
