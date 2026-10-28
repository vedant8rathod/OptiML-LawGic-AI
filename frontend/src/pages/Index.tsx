import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import FeatureCard from "@/components/FeatureCard";
import { Link } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";
import {
  MessageSquare,
  FileText,
  CheckCircle2,
  Globe,
  Shield,
  BarChart3,
  Users,
  Sparkles,
  ArrowRight,
  Scale,
  Heart,
  Lock,
} from "lucide-react";

const Index = () => {
  const { t } = useLanguage();
  const features = [
    {
      icon: MessageSquare,
      title: t('features.askLegalAI.title'),
      description: t('features.askLegalAI.description'),
      badge: t('common.live'),
    },
    {
      icon: FileText,
      title: "Legal Entity Intelligence",
      description: "Extract Indian statutes, court citations, monetary claims, case milestones, relationships, and sanitize sensitive data with privacy redaction.",
      badge: t('common.live'),
      link: "/entities",
    },
    {
      icon: CheckCircle2,
      title: t('features.guidedWorkflow.title'),
      description: t('features.guidedWorkflow.description'),
    },
    {
      icon: Globe,
      title: t('features.multilingual.title'),
      description: t('features.multilingual.description'),
    },
    {
      icon: Shield,
      title: t('features.privacy.title'),
      description: t('features.privacy.description'),
      badge: t('common.certified'),
    },
    {
      icon: BarChart3,
      title: t('features.visualSummaries.title'),
      description: t('features.visualSummaries.description'),
    },
    {
      icon: Users,
      title: t('features.partnerNetwork.title'),
      description: t('features.partnerNetwork.description'),
    },
    {
      icon: Sparkles,
      title: t('features.futureInnovations.title'),
      description: t('features.futureInnovations.description'),
    },
  ];

  const howItWorksSteps = [
    {
      number: "01",
      title: t('howItWorks.step1.title'),
      description: t('howItWorks.step1.description'),
    },
    {
      number: "02",
      title: t('howItWorks.step2.title'),
      description: t('howItWorks.step2.description'),
    },
    {
      number: "03",
      title: t('howItWorks.step3.title'),
      description: t('howItWorks.step3.description'),
    },
  ];

  return (
    <div className="min-h-screen">
      <Header />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
        <div className="absolute inset-0 gradient-hero opacity-5" />
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMzLjMxNCAwIDYgMi42ODYgNiA2cy0yLjY4NiA2LTYgNi02LTIuNjg2LTYtNiAyLjY4Ni02IDYtNnoiIHN0cm9rZT0iY3VycmVudENvbG9yIiBzdHJva2Utd2lkdGg9IjEiIG9wYWNpdHk9Ii4wNSIvPjwvZz48L3N2Zz4=')] opacity-30" />
        
        <div className="container mx-auto max-w-6xl relative z-10">
          <div className="text-center animate-fade-in-up">
            <Badge variant="secondary" className="mb-4 gap-2">
              <Sparkles className="w-3 h-3" />
              {t('hero.badge')}
            </Badge>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-4 tracking-tight">
              <span className="text-black">
                {t('hero.title')}
              </span>
            </h1>
            <p className="text-2xl md:text-3xl font-semibold mb-8 max-w-3xl mx-auto">
              {t('hero.tagline')}
            </p>
            
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed">
              {t('hero.description')}
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button asChild size="lg" className="gap-2 shadow-glow">
                <Link to="/ask-ai">
                  {t('hero.askLegalAI')}
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="gap-2">
                <Link to="#features">
                  {t('hero.exploreFeatures')}
                </Link>
              </Button>
            </div>

            <div className="mt-12 flex items-center justify-center gap-8 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-success" />
                <span>{t('hero.securePrivate')}</span>
              </div>
              <div className="flex items-center gap-2">
                <Globe className="w-4 h-4 text-accent" />
                <span>{t('hero.multilingual')}</span>
              </div>
              <div className="flex items-center gap-2">
                <Heart className="w-4 h-4 text-accent fill-accent" />
                <span>{t('hero.builtForPeople')}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 gradient-subtle">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12 animate-fade-in">
            <Badge variant="secondary" className="mb-4">{t('features.title')}</Badge>
            <h2 className="text-4xl font-bold mb-4">{t('features.subtitle')}</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              {t('features.description')}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-scale-in">
            {features.map((feature, idx) => (
              <FeatureCard key={idx} {...feature} />
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-12 animate-fade-in">
            <Badge variant="secondary" className="mb-4">{t('howItWorks.title')}</Badge>
            <h2 className="text-4xl font-bold mb-4">{t('howItWorks.subtitle')}</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              {t('howItWorks.description')}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 animate-fade-in-up">
            {howItWorksSteps.map((step, idx) => (
              <div key={idx} className="relative">
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-hero flex items-center justify-center text-white font-bold text-xl mb-4 shadow-glow">
                    {step.number}
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
                  <p className="text-muted-foreground">{step.description}</p>
                </div>
                {idx < howItWorksSteps.length - 1 && (
                  <ArrowRight className="hidden md:block absolute top-8 -right-4 w-8 h-8 text-muted-foreground/30" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section id="trust" className="py-20 px-4 sm:px-6 lg:px-8 gradient-subtle">
        <div className="container mx-auto max-w-4xl">
          <div className="text-center mb-12 animate-fade-in">
            <Badge variant="secondary" className="mb-4 gap-2">
              <Lock className="w-3 h-3" />
              {t('trust.title')}
            </Badge>
            <h2 className="text-4xl font-bold mb-4">{t('trust.subtitle')}</h2>
            <p className="text-lg text-muted-foreground">
              {t('trust.description')}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-scale-in">
            <div className="p-6 rounded-2xl gradient-card border border-border/50">
              <div className="w-12 h-12 rounded-xl bg-success/10 flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-success" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{t('trust.encryption.title')}</h3>
              <p className="text-sm text-muted-foreground">
                {t('trust.encryption.description')}
              </p>
            </div>

            <div className="p-6 rounded-2xl gradient-card border border-border/50">
              <div className="w-12 h-12 rounded-xl bg-accent/10 flex items-center justify-center mb-4">
                <Lock className="w-6 h-6 text-accent" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{t('trust.piiRedaction.title')}</h3>
              <p className="text-sm text-muted-foreground">
                {t('trust.piiRedaction.description')}
              </p>
            </div>

            <div className="p-6 rounded-2xl gradient-card border border-border/50">
              <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4">
                <CheckCircle2 className="w-6 h-6 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{t('trust.gdprCompliant.title')}</h3>
              <p className="text-sm text-muted-foreground">
                {t('trust.gdprCompliant.description')}
              </p>
            </div>

            <div className="p-6 rounded-2xl gradient-card border border-border/50">
              <div className="w-12 h-12 rounded-xl bg-warning/10 flex items-center justify-center mb-4">
                <Scale className="w-6 h-6 text-warning" />
              </div>
              <h3 className="text-lg font-semibold mb-2">{t('trust.transparentAI.title')}</h3>
              <p className="text-sm text-muted-foreground">
                {t('trust.transparentAI.description')}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="container mx-auto max-w-4xl">
          <div className="relative overflow-hidden rounded-3xl p-12 text-center gradient-hero shadow-glow animate-scale-in">
            <div className="relative z-10">
              <h2 className="text-4xl font-bold text-white mb-4">
                {t('cta.title')}
              </h2>
              <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
                {t('cta.description')}
              </p>
              <Button asChild size="lg" variant="secondary" className="gap-2 shadow-medium">
                <Link to="/ask-ai">
                  {t('cta.getStarted')}
                  <ArrowRight className="w-4 h-4" />
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default Index;
