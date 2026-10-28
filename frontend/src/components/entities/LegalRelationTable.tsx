import React from "react";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";

export interface LegalRelationItem {
  relation_type: string;
  source: string;
  source_label: string;
  target: string;
  target_label: string;
  supporting_sentence: string;
  confidence: number;
  is_uncertain: boolean;
}

interface LegalRelationTableProps {
  relations: LegalRelationItem[];
}

const RELATION_FORMAT: Record<string, { label: string; color: string }> = {
  represented_by: { label: "represented by", color: "bg-indigo-100 text-indigo-800" },
  heard_by: { label: "heard by", color: "bg-sky-100 text-sky-800" },
  filed_on: { label: "filed on", color: "bg-orange-100 text-orange-800" },
  claims_or_liable_for: { label: "claims / liability", color: "bg-emerald-100 text-emerald-800" },
  cites_or_applies: { label: "cites statute", color: "bg-amber-100 text-amber-800" },
  contained_in: { label: "contained in", color: "bg-teal-100 text-teal-800" },
};

const LegalRelationTable: React.FC<LegalRelationTableProps> = ({ relations }) => {
  if (!relations || relations.length === 0) {
    return (
      <div className="p-8 text-center text-muted-foreground text-sm border rounded-xl bg-card">
        No relational links detected across extracted entities.
      </div>
    );
  }

  return (
    <div className="border border-border/70 rounded-xl overflow-hidden shadow-sm bg-card">
      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-muted/70 text-muted-foreground uppercase text-[10px] tracking-wider border-b border-border">
            <tr>
              <th className="py-2.5 px-3 font-semibold">Subject / Entity</th>
              <th className="py-2.5 px-3 font-semibold text-center">Relationship</th>
              <th className="py-2.5 px-3 font-semibold">Object / Target</th>
              <th className="py-2.5 px-3 font-semibold">Supporting Evidentiary Context</th>
              <th className="py-2.5 px-3 font-semibold text-center">Certainty</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/60">
            {relations.map((rel, idx) => {
              const relMeta = RELATION_FORMAT[rel.relation_type] || {
                label: rel.relation_type.replace(/_/g, " "),
                color: "bg-gray-100 text-gray-800",
              };

              return (
                <tr key={idx} className="hover:bg-muted/30 transition-smooth">
                  <td className="py-2.5 px-3 font-medium text-foreground">
                    <div>{rel.source}</div>
                    <span className="text-[10px] text-muted-foreground uppercase">
                      {rel.source_label}
                    </span>
                  </td>

                  <td className="py-2.5 px-3 text-center whitespace-nowrap">
                    <span className={`px-2 py-0.5 rounded-full font-semibold uppercase text-[10px] ${relMeta.color}`}>
                      {relMeta.label}
                    </span>
                  </td>

                  <td className="py-2.5 px-3 font-medium text-foreground">
                    <div>{rel.target}</div>
                    <span className="text-[10px] text-muted-foreground uppercase">
                      {rel.target_label}
                    </span>
                  </td>

                  <td className="py-2.5 px-3 text-muted-foreground max-w-xs truncate italic" title={rel.supporting_sentence}>
                    "{rel.supporting_sentence}"
                  </td>

                  <td className="py-2.5 px-3 text-center">
                    {rel.is_uncertain ? (
                      <Badge variant="outline" className="text-[10px] text-amber-600 gap-1 border-amber-300">
                        <AlertCircle className="w-3 h-3" />
                        Uncertain
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="text-[10px] text-emerald-600 gap-1 border-emerald-300">
                        <CheckCircle2 className="w-3 h-3" />
                        Confirmed
                      </Badge>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default LegalRelationTable;
