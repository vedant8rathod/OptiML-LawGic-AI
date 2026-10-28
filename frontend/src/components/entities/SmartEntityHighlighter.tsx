import React, { useMemo } from "react";

export interface EntityOccurrence {
  start: number;
  end: number;
  text: string;
}

export interface EntityItem {
  text: string;
  normalized?: string;
  label: string;
  confidence?: number;
  source?: string;
  start: number;
  end: number;
}

interface SmartEntityHighlighterProps {
  text: string;
  entities: EntityItem[];
  selectedEntity: EntityItem | null;
  onSelectEntity: (entity: EntityItem) => void;
  filterCategory: string;
}

export const CATEGORY_STYLES: Record<string, { bg: string; text: string; border: string }> = {
  PERSON: { bg: "bg-purple-100", text: "text-purple-800", border: "border-purple-300" },
  ADVOCATE: { bg: "bg-indigo-100", text: "text-indigo-800", border: "border-indigo-300" },
  JUDGE: { bg: "bg-violet-100", text: "text-violet-800", border: "border-violet-300" },
  LEGAL_ROLE: { bg: "bg-fuchsia-100", text: "text-fuchsia-800", border: "border-fuchsia-300" },
  ORGANIZATION: { bg: "bg-blue-100", text: "text-blue-800", border: "border-blue-300" },
  COURT: { bg: "bg-sky-100", text: "text-sky-800", border: "border-sky-300" },
  LOCATION: { bg: "bg-cyan-100", text: "text-cyan-800", border: "border-cyan-300" },
  STATUTE: { bg: "bg-emerald-100", text: "text-emerald-800", border: "border-emerald-300" },
  LEGAL_PROVISION: { bg: "bg-teal-100", text: "text-teal-800", border: "border-teal-300" },
  CASE_NUMBER: { bg: "bg-amber-100", text: "text-amber-800", border: "border-amber-300" },
  MONEY: { bg: "bg-green-100", text: "text-green-800", border: "border-green-300" },
  PERCENTAGE: { bg: "bg-lime-100", text: "text-lime-800", border: "border-lime-300" },
  DATE: { bg: "bg-orange-100", text: "text-orange-800", border: "border-orange-300" },
  LEGAL_EVENT: { bg: "bg-rose-100", text: "text-rose-800", border: "border-rose-300" },
  EMAIL: { bg: "bg-pink-100", text: "text-pink-800", border: "border-pink-300" },
  PHONE: { bg: "bg-red-100", text: "text-red-800", border: "border-red-300" },
};

const SmartEntityHighlighter: React.FC<SmartEntityHighlighterProps> = ({
  text,
  entities,
  selectedEntity,
  onSelectEntity,
  filterCategory,
}) => {
  const renderedSegments = useMemo(() => {
    if (!text) return null;

    // Filter by selected category if any
    const activeEntities = filterCategory === "ALL"
      ? entities
      : entities.filter((e) => e.label === filterCategory);

    // Sort by start index
    const sorted = [...activeEntities].sort((a, b) => a.start - b.start);

    const segments: React.ReactNode[] = [];
    let currentIndex = 0;

    sorted.forEach((ent, idx) => {
      // Non-entity gap text
      if (ent.start > currentIndex) {
        segments.push(
          <span key={`text-${currentIndex}`}>
            {text.substring(currentIndex, ent.start)}
          </span>
        );
      }

      // Check if entity is selected
      const isSelected = selectedEntity && selectedEntity.start === ent.start && selectedEntity.end === ent.end;
      const style = CATEGORY_STYLES[ent.label] || { bg: "bg-gray-100", text: "text-gray-800", border: "border-gray-300" };

      segments.push(
        <button
          key={`ent-${idx}-${ent.start}`}
          type="button"
          onClick={() => onSelectEntity(ent)}
          className={`inline-block px-1.5 py-0.5 rounded text-xs font-medium border transition-all cursor-pointer ${
            style.bg
          } ${style.text} ${style.border} ${
            isSelected ? "ring-2 ring-primary ring-offset-1 font-bold shadow-sm" : "hover:brightness-95"
          }`}
          title={`${ent.label} (Click for details)`}
        >
          {ent.text}
          <span className="ml-1 text-[10px] opacity-75 uppercase">
            {ent.label.replace("LEGAL_", "")}
          </span>
        </button>
      );

      currentIndex = ent.end;
    });

    // Remainder text
    if (currentIndex < text.length) {
      segments.push(
        <span key={`text-${currentIndex}`}>{text.substring(currentIndex)}</span>
      );
    }

    return segments;
  }, [text, entities, selectedEntity, filterCategory, onSelectEntity]);

  return (
    <div className="bg-card border border-border/70 rounded-xl p-5 shadow-sm text-sm leading-relaxed font-sans whitespace-pre-wrap max-h-[550px] overflow-y-auto">
      {renderedSegments || <p className="text-muted-foreground italic">No document text available.</p>}
    </div>
  );
};

export default SmartEntityHighlighter;
