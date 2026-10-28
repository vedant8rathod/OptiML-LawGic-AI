import React from "react";
import { Badge } from "@/components/ui/badge";
import { CATEGORY_STYLES, EntityItem } from "./SmartEntityHighlighter";
import { X, ExternalLink, ShieldCheck } from "lucide-react";

interface EntityDetailPanelProps {
  entity: EntityItem | null;
  allOccurrences: Array<{ start: number; end: number; text: string }>;
  onClose: () => void;
  onJumpToOccurrence: (start: number, end: number) => void;
}

const EntityDetailPanel: React.FC<EntityDetailPanelProps> = ({
  entity,
  allOccurrences,
  onClose,
  onJumpToOccurrence,
}) => {
  if (!entity) return null;

  const style = CATEGORY_STYLES[entity.label] || {
    bg: "bg-gray-100",
    text: "text-gray-800",
    border: "border-gray-300",
  };

  return (
    <div className="border border-border/80 rounded-xl p-4 bg-card shadow-sm space-y-3">
      <div className="flex items-center justify-between pb-2 border-b border-border/50">
        <div className="flex items-center gap-2">
          <span className={`px-2 py-0.5 rounded text-xs font-semibold uppercase ${style.bg} ${style.text}`}>
            {entity.label}
          </span>
          {entity.confidence !== undefined && (
            <Badge variant="outline" className="text-[11px] h-5 gap-1">
              <ShieldCheck className="w-3 h-3 text-emerald-600" />
              {(entity.confidence * 100).toFixed(0)}% Conf.
            </Badge>
          )}
        </div>
        <button
          onClick={onClose}
          className="text-muted-foreground hover:text-foreground transition-smooth p-1"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div>
        <h3 className="font-semibold text-base text-foreground break-words">{entity.text}</h3>
        {entity.normalized && entity.normalized !== entity.text && (
          <p className="text-xs text-muted-foreground mt-0.5">
            Normalized: <span className="font-mono text-foreground">{entity.normalized}</span>
          </p>
        )}
      </div>

      <div>
        <h4 className="text-xs font-medium text-muted-foreground mb-1.5 uppercase">
          Detected Mentions ({allOccurrences.length})
        </h4>
        <div className="space-y-1.5 max-h-36 overflow-y-auto">
          {allOccurrences.map((occ, idx) => (
            <button
              key={`${occ.start}-${idx}`}
              type="button"
              onClick={() => onJumpToOccurrence(occ.start, occ.end)}
              className="w-full text-left text-xs p-2 rounded-lg bg-muted/60 hover:bg-muted transition-smooth flex items-center justify-between group"
            >
              <span className="truncate pr-2 font-mono">
                Offset [{occ.start} : {occ.end}]
              </span>
              <ExternalLink className="w-3.5 h-3.5 text-muted-foreground group-hover:text-primary shrink-0" />
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default EntityDetailPanel;
