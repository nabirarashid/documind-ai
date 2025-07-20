interface FeatureCardProps { 
    icon: React.ComponentType<React.SVGProps<SVGSVGElement>>;
    title: string;
    description: string;
    gradient: string;
    }

const FeatureCard = ({ icon: Icon, title, description, gradient }: FeatureCardProps) => (
  <div className={`relative overflow-hidden rounded-xl p-6 ${gradient} text-white group hover:scale-105 transition-transform duration-300`}>
    <div className="absolute inset-0 bg-black/10 group-hover:bg-black/20 transition-colors duration-300"></div>
    <div className="relative z-10">
      <Icon className="h-8 w-8 mb-4" />
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-sm opacity-90">{description}</p>
    </div>
  </div>
);

export default FeatureCard;