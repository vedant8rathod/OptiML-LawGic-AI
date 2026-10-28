import React from "react";
import { Badge } from "@/components/ui/badge";
import { Calendar, UserCheck } from "lucide-react";

export interface TimelineEventItem {
  date: string;
  normalized_date?: string;
  event_description: string;
  involved_entities: string[];
  supporting_text: string;
  start_offset: number;
  end_offset: number;
  is_explicit: boolean;
}

interface LegalTimelineProps {
  timeline: TimelineEventItem[];
  onSelectEvent?: (start: number, end: number) => void;
}

const LegalTimeline: React.FC<LegalTimelineProps> = ({ timeline, onSelectEvent }) => {
  if (!timeline || timeline.length === 0) {
    return (
      <div className="p-8 text-center text-muted-foreground text-sm border rounded-xl bg-card">
        No chronological dates or legal event milestones detected in document.
      </div>
    );
  }

  return (
    <div className="relative border-l-2 border-primary/30 pl-5 space-y-6 my-2 ml-3">
      {timeline.map((evt, idx) => (
        <div key={idx} className="relative group">
          {/* Timeline Dot */}
          <div className="absolute -left-[27px] top-1.5 w-3.5 h-3.5 rounded-full bg-primary border-2 border-background ring-2 ring-primary/20 group-hover:scale-125 transition-transform" />

          <div
            onClick={() => onSelectEvent?.(evt.start_offset, evt.end_offset)}
            className="p-3.5 rounded-xl border border-border/70 bg-card hover:border-primary/50 shadow-sm transition-all cursor-pointer"
          >
            <div className="flex items-center justify-between gap-2 mb-1.5">
              <span className="inline-flex items-center gap-1.5 text-xs font-semibold text-primary">
                <Calendar className="w-3.5 h-3.5" />
                {evt.date}
              </span>
              <Badge variant="secondary" className="text-[10px]">
                {evt.is_explicit ? "Explicit Date" : "Inferred"}
              </Badge>
            </div>

            <p className="text-xs font-medium text-foreground mb-2 leading-relaxed">
              {evt.event_description}
            </p>

            {evt.involved_entities.length > 0 && (
              <div className="flex flex-wrap items-center gap-1 mt-2 pt-2 border-t border-border/40">
                <span className="text-[10px] text-muted-foreground mr-1">Involved:</span>
                {evt.involved_entities.map((e, eIdx) => (
                  <Badge key={eIdx} variant="outline" className="text-[10px] px-1.5 py-0 h-4.5 bg-muted/40">
                    {e}
                  </Badge>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default LegalTimeline;
