import { LucideIcon } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Link } from "react-router-dom";

interface FeatureCardProps {
  icon: LucideIcon;
  title: string;
  description: string;
  badge?: string;
  link?: string;
}

const FeatureCard = ({ icon: Icon, title, description, badge, link }: FeatureCardProps) => {
  const content = (
    <Card className="gradient-card p-6 hover-lift border-border/50 relative overflow-hidden group h-full">
      <div className="absolute inset-0 bg-gradient-hero opacity-0 group-hover:opacity-5 transition-smooth" />
      
      {badge && (
        <span className="absolute top-4 right-4 text-xs font-medium px-2 py-1 rounded-full bg-accent/10 text-accent">
          {badge}
        </span>
      )}
      
      <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:scale-110 transition-smooth">
        <Icon className="w-6 h-6 text-primary" />
      </div>
      
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
    </Card>
  );

  if (link) {
    return <Link to={link} className="block h-full">{content}</Link>;
  }

  return content;
};

export default FeatureCard;
