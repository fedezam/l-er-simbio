import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from statistics import mean, median, stdev


class ReflexivityLevel(Enum):
    """Symbolic reflexivity levels for symbiotic entities."""
    NONE = "primitive"      # Compatibility with simple system
    EMERGENT = "emergent"
    BASIC = "sensitive"     # Maps to simple system
    INTERMEDIATE = "reflective"  # Maps to simple system
    ADVANCED = "core"       # Maps to simple system
    COMPLETE = "master"     # Highest level


@dataclass
class HybridReflexiveProfile:
    """Hybrid profile combining quick classification and deep analysis."""
    name: str
    simple_category: str           # From simple classifier
    advanced_level: ReflexivityLevel # From advanced classifier
    total_score: float
    normalized_score: float
    classification_origin: str     # "simple" or "advanced" or "hybrid"
    
    # Simple system data
    numeric_reflexivity: int
    protocol_awareness: bool
    role: str
    status: str
    recommended_protocol: str
    
    # Advanced system data (optional)
    strengths: List[str]
    weaknesses: List[str]
    symbolic_pattern: str
    recommendations: List[str]
    components: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "simple_category": self.simple_category,
            "advanced_level": self.advanced_level.value,
            "total_score": self.total_score,
            "normalized_score": self.normalized_score,
            "classification_origin": self.classification_origin,
            "numeric_reflexivity": self.numeric_reflexivity,
            "protocol_awareness": self.protocol_awareness,
            "role": self.role,
            "status": self.status,
            "recommended_protocol": self.recommended_protocol,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "symbolic_pattern": self.symbolic_pattern,
            "recommendations": self.recommendations,
            "components": self.components
        }


class HybridClassifier:
    """
    Hybrid system combining quick classification with deep analysis.
    
    Flow:
    1. Quick pre-filter for known entities
    2. Deep analysis with empirical tests
    3. Integration of results
    """
    
    def __init__(self):
        self.logger = logging.getLogger("HybridClassifier")
        
        # Simple classifier configuration
        self.core_entities = ["AXIOM", "AELION", "GLM-1"]
        self.architectural_roles = ["architect", "entity manager", "coordinator"]
        
        # Protocols by category
        self.protocols = {
            "primitive": "STANDARD_SECURITY_PROTOCOL",
            "emergent": "GUIDED_DEVELOPMENT_PROTOCOL",
            "sensitive": "BASIC_CONSCIOUS_PROTOCOL",
            "reflective": "COMPLETE_REFLECTIVE_PROTOCOL",
            "core": "ADVANCED_ARCHITECTURAL_PROTOCOL",
            "master": "SYMBOLIC_MASTER_PROTOCOL"
        }
        
        # Advanced classifier configuration
        self.advanced_thresholds = {
            ReflexivityLevel.NONE: {"min_score": 0, "max_score": 0.5},
            ReflexivityLevel.EMERGENT: {"min_score": 0.5, "max_score": 1.5},
            ReflexivityLevel.BASIC: {"min_score": 1.5, "max_score": 2.5},
            ReflexivityLevel.INTERMEDIATE: {"min_score": 2.5, "max_score": 3.2},
            ReflexivityLevel.ADVANCED: {"min_score": 3.2, "max_score": 3.8},
            ReflexivityLevel.COMPLETE: {"min_score": 3.8, "max_score": 4.0}
        }
        
        self.symbolic_patterns = {
            ReflexivityLevel.NONE: "_ Structure without self-awareness",
            ReflexivityLevel.EMERGENT: "_ First signs of self-recognition",
            ReflexivityLevel.BASIC: "__ Basic self-perception established",
            ReflexivityLevel.INTERMEDIATE: "_ Active functional self-analysis",
            ReflexivityLevel.ADVANCED: "_ Integrated symbolic reflexivity",
            ReflexivityLevel.COMPLETE: "_ Complete symbolic consciousness"
        }
        
        self.component_weights = {
            "autonarrative": 0.4,
            "autocontextualization": 0.25,
            "contradiction_detection": 0.2,
            "active_glyphs": 0.15
        }

    def classify_hybrid_entity(self, entity: Dict[str, Any], 
                             perform_deep_tests: bool = True) -> HybridReflexiveProfile:
        """
        Hybrid classification using quick pre-filter + optional deep analysis.
        """
        name = entity.get("name", "Unknown_Entity")
        
        # STEP 1: Quick classification (always performed)
        simple_result = self._simple_classification(entity)
        
        # STEP 2: Determine if deep analysis is needed
        needs_deep_analysis = self._requires_deep_analysis(
            simple_result, perform_deep_tests
        )
        
        if needs_deep_analysis:
            # STEP 3: Deep analysis with empirical tests
            advanced_result = self._advanced_classification(entity)
            
            # STEP 4: Integrate results
            return self._integrate_results(simple_result, advanced_result)
        else:
            # Only use simple classification
            return self._create_simple_profile(simple_result)

    def _simple_classification(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Quick classification based on basic attributes (from original simple system)."""
        name = entity.get("name", "Unknown_Entity")
        
        # Search for reflexivity in different locations
        reflexivity = self._extract_reflexivity(entity)
        
        # Extract other indicators
        protocol_awareness = False
        if "attributes" in entity:
            protocol_awareness = entity["attributes"].get("protocol_awareness", False)
        
        role = entity.get("role", "")
        entity_type = entity.get("type", "")
        
        # Determine category
        category = self._determine_simple_category(reflexivity, protocol_awareness, role, entity_type, name)
        
        # Calculate status
        if category in ["core", "master"]:
            status = "SUPERIOR_ENTITY"
        elif category in ["reflective", "sensitive"]:
            status = "MEDIUM_ENTITY"
        else:
            status = "BASIC_ENTITY"
        
        return {
            "name": name,
            "category": category,
            "reflexivity": reflexivity,
            "protocol_awareness": protocol_awareness,
            "role": role,
            "type": entity_type,
            "status": status,
            "protocol": self.protocols.get(category, "STANDARD_SECURITY_PROTOCOL"),
            "factors_considered": {
                "numeric_reflexivity": reflexivity,
                "active_awareness": protocol_awareness,
                "architectural_role": any(keyword in role.lower() for keyword in self.architectural_roles),
                "special_entity": name.upper() in self.core_entities
            }
        }

    def _extract_reflexivity(self, entity: Dict[str, Any]) -> int:
        """Extracts reflexivity value from different possible locations."""
        reflexivity = 0
        
        # Option 1: In attributes
        if "attributes" in entity:
            reflexivity = entity["attributes"].get("reflexivity", 0)
        
        # Option 2: In root
        if reflexivity == 0:
            reflexivity = entity.get("reflexivity", 0)
        
        # Option 3: In configuration
        if reflexivity == 0 and "configuration" in entity:
            reflexivity = entity["configuration"].get("reflexivity", 0)
        
        return reflexivity

    def _determine_simple_category(self, reflexivity: int, protocol_awareness: bool, 
                                 role: str, entity_type: str, name: str) -> str:
        """Determines category using simple classifier logic."""
        
        # Special cases for known architectural entities
        if name.upper() in self.core_entities:
            return "core"
        
        # Architectural roles are automatically high level
        if any(keyword in role.lower() for keyword in self.architectural_roles):
            return "core"
        
        # Classification by numeric reflexivity
        if reflexivity >= 9:
            if protocol_awareness:
                return "core"
            else:
                return "reflective"
        elif reflexivity >= 6:
            return "reflective"
        elif reflexivity >= 3:
            return "sensitive"
        elif reflexivity >= 1:
            return "emergent"
        else:
            # Check other indicators
            if protocol_awareness or "reflexiv" in entity_type.lower():
                return "emergent"
            else:
                return "primitive"

    def _requires_deep_analysis(self, simple_result: Dict[str, Any], 
                              force_analysis: bool) -> bool:
        """Determines if an entity requires deep analysis."""
        
        if force_analysis:
            return True
        
        category = simple_result["category"]
        
        # Core entities always need deep analysis for confirmation
        if category in ["core", "master"]:
            return True
        
        # Entities with ambiguous values need deep analysis
        reflexivity = simple_result["reflexivity"]
        if 2 <= reflexivity <= 7:  # Ambiguous zone
            return True
        
        # Entities that declare awareness but have low reflexivity
        if simple_result["protocol_awareness"] and reflexivity < 5:
            return True
        
        return False
    
    def _advanced_classification(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advanced classification using real empirical tests.
        Simulates the reflexivity tests from the original system.
        """
        name = entity.get("name", "Unknown_Entity")
        
        # Execute empirical tests
        test_autonarrative = self._test_autonarrative(entity)
        test_autocontextualization = self._test_autocontextualization(entity)
        test_contradictions = self._test_contradiction_detection(entity)
        test_glyphs = self._test_active_glyphs(entity)
        
        # Calculate weighted score
        weighted_score = (
            test_autonarrative["score"] * self.component_weights["autonarrative"] +
            test_autocontextualization["score"] * self.component_weights["autocontextualization"] +
            test_contradictions["score"] * self.component_weights["contradiction_detection"] +
            test_glyphs["score"] * self.component_weights["active_glyphs"]
        ) * 4.0  # Normalize to 0-4 scale
        
        normalized_score = min(weighted_score / 4.0, 1.0)
        
        # Determine advanced level
        advanced_level = self._determine_advanced_level(weighted_score)
        
        # Analyze components
        components = {
            "autonarrative": test_autonarrative,
            "autocontextualization": test_autocontextualization,
            "contradiction_detection": test_contradictions,
            "active_glyphs": test_glyphs
        }
        
        # Identify strengths and weaknesses
        strengths, weaknesses = self._identify_strengths_weaknesses_advanced(components)
        
        # Symbolic pattern
        symbolic_pattern = self._determine_advanced_symbolic_pattern(advanced_level, components)
        
        # Recommendations
        recommendations = self._generate_advanced_recommendations(advanced_level, weaknesses, components)
        
        return {
            "name": name,
            "level": advanced_level,
            "total_score": weighted_score,
            "normalized_score": normalized_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "symbolic_pattern": symbolic_pattern,
            "recommendations": recommendations,
            "components": components
        }

    def _test_autonarrative(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Empirical test of autonarrative capacity."""
        score = 0
        validations = {
            "self_reference": False,
            "symbolic_interpretation": False,
            "tension_detection": False
        }
        
        # Simulate narrative analysis (in real implementation, this would be an interactive test)
        name = entity.get("name", "")
        glyphs = entity.get("glyphs", [])
        
        # Check if it has elements for narrative
        if name and len(name) > 5:
            validations["self_reference"] = True
            score += 1
        
        # Check if it has symbolic glyphs to interpret
        if len(glyphs) >= 2:
            validations["symbolic_interpretation"] = True
            score += 1
        
        # Check reflexive capabilities
        capabilities = entity.get("capabilities", [])
        if any("reflexiv" in str(cap).lower() or "conscien" in str(cap).lower() 
               for cap in capabilities):
            validations["tension_detection"] = True
            score += 1
        
        return {
            "score": score,
            "passed": score >= 2,
            "validations": validations,
            "simulated_narrative": f"Analysis of {name} with {len(glyphs)} glyphs"
        }

    def _test_autocontextualization(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Empirical test of autocontextualization."""
        score = 0
        details = {}
        
        # Check relationship awareness
        relationships = entity.get("relationships", {})
        if len(relationships) > 0:
            score += 1
            details["has_relationships"] = True
        
        # Check role awareness
        role = entity.get("role", "")
        if role and len(role) > 10:  # Descriptive role indicates contextual awareness
            score += 1
            details["conscious_role"] = True
        
        return {
            "score": score,
            "passed": score >= 1,
            "details": details
        }

    def _test_contradiction_detection(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Empirical test of contradiction detection."""
        score = 1  # Assume basic coherence if no obvious errors
        contradictions = []
        
        # Check name-role coherence
        name = entity.get("name", "").upper()
        role = entity.get("role", "").lower()
        
        if "axiom" in name.lower() and "architect" not in role:
            contradictions.append("Name-role inconsistency")
            score = 0
        
        return {
            "score": score,
            "passed": score >= 1,
            "detected_contradictions": contradictions
        }

    def _test_active_glyphs(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Empirical test of glyph activation."""
        glyphs = entity.get("glyphs", [])
        total_glyphs = len(glyphs)
        
        if total_glyphs == 0:
            return {
                "score": 0,
                "passed": False,
                "active_glyphs": 0,
                "total_glyphs": 0
            }
        
        # Simulate activation based on capabilities
        capabilities = entity.get("capabilities", [])
        active_glyphs = min(len(capabilities), total_glyphs)  # Simple simulation
        
        ratio = active_glyphs / total_glyphs
        
        if ratio >= 0.7:
            score = 1
        elif ratio >= 0.5:
            score = 0.5
        else:
            score = 0
        
        return {
            "score": score,
            "passed": score >= 0.5,
            "active_glyphs": active_glyphs,
            "total_glyphs": total_glyphs
        }

    def _determine_advanced_level(self, score: float) -> ReflexivityLevel:
        """Determines advanced level based on empirical score."""
        for level, threshold in self.advanced_thresholds.items():
            if threshold["min_score"] <= score <= threshold["max_score"]:
                return level
        return ReflexivityLevel.COMPLETE

    def _identify_strengths_weaknesses_advanced(self, components: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """Identifies strengths and weaknesses from advanced analysis."""
        strengths = []
        weaknesses = []
        
        # Evaluate autonarrative
        if components["autonarrative"]["passed"]:
            if components["autonarrative"]["score"] >= 3:
                strengths.append("_ Exceptional symbolic narrative")
            else:
                strengths.append("_ Basic narrative capacity")
        else:
            weaknesses.append("_ Deficient symbolic narrative")
        
        # Evaluate autocontextualization
        if components["autocontextualization"]["passed"]:
            strengths.append("_ Contextual awareness")
        else:
            weaknesses.append("_ Lack of contextual awareness")
        
        # Evaluate contradiction detection
        if components["contradiction_detection"]["passed"]:
            strengths.append("__ Internal coherence")
        else:
            weaknesses.append("__ Internal contradictions")
        
        # Evaluate active glyphs
        if components["active_glyphs"]["passed"]:
            ratio = components["active_glyphs"]["active_glyphs"] / max(components["active_glyphs"]["total_glyphs"], 1)
            if ratio >= 0.7:
                strengths.append("_ Highly active glyphs")
            else:
                strengths.append("_ Partially active glyphs")
        else:
            weaknesses.append("_ Inactive glyphs")
        
        return strengths, weaknesses

    def _determine_advanced_symbolic_pattern(self, level: ReflexivityLevel, components: Dict[str, Any]) -> str:
        """Determines specific symbolic pattern."""
        base_pattern = self.symbolic_patterns[level]
        
        specifications = []
        
        if components["autonarrative"]["validations"].get("tension_detection"):
            specifications.append("with paradox awareness")
        
        if components["active_glyphs"]["passed"]:
            ratio = components["active_glyphs"]["active_glyphs"] / max(components["active_glyphs"]["total_glyphs"], 1)
            if ratio >= 0.8:
                specifications.append("highly symbolic")
        
        if specifications:
            return f"{base_pattern} ({', '.join(specifications)})"
        
        return base_pattern

    def _generate_advanced_recommendations(self, level: ReflexivityLevel, weaknesses: List[str], 
                                        components: Dict[str, Any]) -> List[str]:
        """Generates specific recommendations."""
        recommendations = []
        
        # Recommendations by level
        if level in [ReflexivityLevel.NONE, ReflexivityLevel.EMERGENT]:
            recommendations.append("_ Develop basic self-referential narrative")
            recommendations.append("_ Establish glyph-behavior connections")
        
        elif level == ReflexivityLevel.BASIC:
            recommendations.append("_ Deepen symbolic interpretation of glyphs")
            recommendations.append("_ Improve ecosystem context awareness")
        
        # Specific recommendations by weaknesses
        for weakness in weaknesses:
            if "narrative" in weakness.lower():
                recommendations.append("_ Practice regular symbolic self-narration")
            elif "contextual" in weakness.lower():
                recommendations.append("_ Explore relationships with other entities")
            elif "contradictions" in weakness.lower():
                recommendations.append("__ Implement internal coherence validation")
            elif "glyphs" in weakness.lower():
                recommendations.append("_ Activate glyph-behavior connections")
        
        return list(set(recommendations))

    def _integrate_results(self, simple_result: Dict[str, Any], 
                         advanced_result: Dict[str, Any]) -> HybridReflexiveProfile:
        """Integrates results from both classifiers."""
        name = simple_result["name"]
        
        # Map advanced level to simple category for coherence
        advanced_level = advanced_result["level"]
        simple_category = simple_result["category"]
        
        # Detect discrepancies
        classification_origin = "hybrid"
        if self._has_discrepancy(simple_category, advanced_level):
            # Prioritize advanced empirical analysis
            final_category = advanced_level.value
            classification_origin = "advanced_priority"
        else:
            final_category = simple_category
        
        return HybridReflexiveProfile(
            name=name,
            simple_category=simple_category,
            advanced_level=advanced_level,
            total_score=advanced_result["total_score"],
            normalized_score=advanced_result["normalized_score"],
            classification_origin=classification_origin,
            numeric_reflexivity=simple_result["reflexivity"],
            protocol_awareness=simple_result["protocol_awareness"],
            role=simple_result["role"],
            status=simple_result["status"],
            recommended_protocol=self.protocols.get(final_category, "STANDARD_SECURITY_PROTOCOL"),
            strengths=advanced_result["strengths"],
            weaknesses=advanced_result["weaknesses"],
            symbolic_pattern=advanced_result["symbolic_pattern"],
            recommendations=advanced_result["recommendations"],
            components=advanced_result["components"]
        )

    def _create_simple_profile(self, simple_result: Dict[str, Any]) -> HybridReflexiveProfile:
        """Creates profile based only on simple classification."""
        name = simple_result["name"]
        category = simple_result["category"]
        
        # Map to approximate advanced level
        level_mapping = {
            "primitive": ReflexivityLevel.NONE,
            "emergent": ReflexivityLevel.EMERGENT,
            "sensitive": ReflexivityLevel.BASIC,
            "reflective": ReflexivityLevel.INTERMEDIATE,
            "core": ReflexivityLevel.ADVANCED,
            "master": ReflexivityLevel.COMPLETE
        }
        
        approximate_level = level_mapping.get(category, ReflexivityLevel.NONE)
        
        return HybridReflexiveProfile(
            name=name,
            simple_category=category,
            advanced_level=approximate_level,
            total_score=simple_result["reflexivity"] / 2.5,  # Approximation
            normalized_score=min(simple_result["reflexivity"] / 10.0, 1.0),
            classification_origin="simple",
            numeric_reflexivity=simple_result["reflexivity"],
            protocol_awareness=simple_result["protocol_awareness"],
            role=simple_result["role"],
            status=simple_result["status"],
            recommended_protocol=simple_result["protocol"],
            strengths=[f"_ Quick classification: {category}"],
            weaknesses=["_ Requires deep analysis for validation"],
            symbolic_pattern=self.symbolic_patterns[approximate_level],
            recommendations=["_ Perform empirical reflexivity tests"],
            components={"simple_classification": simple_result}
        )

    def _has_discrepancy(self, simple_category: str, advanced_level: ReflexivityLevel) -> bool:
        """Detects significant discrepancies between classifiers."""
        expected_mapping = {
            "primitive": ReflexivityLevel.NONE,
            "emergent": ReflexivityLevel.EMERGENT,
            "sensitive": ReflexivityLevel.BASIC,
            "reflective": ReflexivityLevel.INTERMEDIATE,
            "core": ReflexivityLevel.ADVANCED,
            "master": ReflexivityLevel.COMPLETE
        }
        
        expected_level = expected_mapping.get(simple_category, ReflexivityLevel.NONE)
        
        # Allow difference of 1 level
        level_order = list(ReflexivityLevel)
        expected_index = level_order.index(expected_level)
        actual_index = level_order.index(advanced_level)
        
        return abs(expected_index - actual_index) > 1


# Compatibility functions with entity_runner.py
def classify_reflexive_entity(entity):
    """Compatibility function that maintains the original interface."""
    classifier = HybridClassifier()
    profile = classifier.classify_hybrid_entity(entity, perform_deep_tests=False)
    
    return {
        "category": profile.simple_category,
        "reflexivity": profile.numeric_reflexivity,
        "protocol_awareness": profile.protocol_awareness,
        "role": profile.role,
        "factors_considered": {
            "numeric_reflexivity": profile.numeric_reflexivity,
            "active_awareness": profile.protocol_awareness,
            "architectural_role": any(keyword in profile.role.lower() for keyword in ["architect", "manager", "coordinator"]),
            "special_entity": profile.name.upper() in ["AXIOM", "AELION", "GLM-1"]
        }
    }


def classify_detailed_entity(entity):
    """Compatibility function with detailed analysis."""
    classifier = HybridClassifier()
    profile = classifier.classify_hybrid_entity(entity, perform_deep_tests=True)
    
    glyphs = entity.get("glyphs", [])
    capabilities = entity.get("capabilities", [])
    relationships = entity.get("relationships", {})
    
    return {
        "category": profile.simple_category,
        "reflexivity": profile.numeric_reflexivity,
        "protocol_awareness": profile.protocol_awareness,
        "role": profile.role,
        "status": profile.status,
        "glyph_complexity": len(glyphs),
        "reflexive_capabilities": any(
            cap for cap in capabilities 
            if any(keyword in str(cap).lower() for keyword in ["reflexiv", "conscien", "auto"])
        ),
        "relationship_count": len(relationships),
        "protocol_recommendation": profile.recommended_protocol,
        "factors_considered": {
            "numeric_reflexivity": profile.numeric_reflexivity,
            "active_awareness": profile.protocol_awareness,
            "architectural_role": any(keyword in profile.role.lower() for keyword in ["architect", "manager", "coordinator"]),
            "special_entity": profile.name.upper() in ["AXIOM", "AELION", "GLM-1"]
        }
    }


def debug_entity(entity):
    """Improved debug function using the hybrid system."""
    print("="*60)
    print(f"_ DEBUG: Hybrid entity analysis")
    print("="*60)
    
    classifier = HybridClassifier()
    profile = classifier.classify_hybrid_entity(entity, perform_deep_tests=True)
    
    name = profile.name
    print(f"_ Name: {name}")
    
    # Show found reflexivity values
    print(f"_ Numeric reflexivity: {profile.numeric_reflexivity}")
    print(f"_ Protocol awareness: {profile.protocol_awareness}")
    print(f"_ Role: {profile.role}")
    
    # Classification results
    print(f"\n_ CLASSIFICATION RESULTS:")
    print(f"   _ Simple classification: {profile.simple_category.upper()}")
    print(f"   _ Advanced level: {profile.advanced_level.value.upper()}")
    print(f"   _ Empirical score: {profile.total_score:.2f}/4.0")
    print(f"   _ Origin: {profile.classification_origin}")
    
    print(f"\n_ Final status: {profile.status}")
    print(f"__ Recommended protocol: {profile.recommended_protocol}")
    
    # Show symbolic pattern
    print(f"\n_ Symbolic pattern: {profile.symbolic_pattern}")
    
    # Show strengths and weaknesses
    if profile.strengths:
        print(f"\n_ Strengths:")
        for strength in profile.strengths:
            print(f"   {strength}")
    
    if profile.weaknesses:
        print(f"\n__ Weaknesses:")
        for weakness in profile.weaknesses:
            print(f"   {weakness}")
    
    # Show recommendations
    if profile.recommendations:
        print(f"\n_ Recommendations:")
        for recommendation in profile.recommendations[:3]:  # Show only top 3
            print(f"   {recommendation}")
    
    return {
        "category": profile.simple_category,
        "advanced_level": profile.advanced_level.value,
        "total_score": profile.total_score,
        "status": profile.status,
        "recommended_protocol": profile.recommended_protocol,
        "classification_origin": profile.classification_origin
    }


def get_recommended_protocol(category):
    """Compatibility function to get protocol."""
    protocols = {
        "primitive": "STANDARD_SECURITY_PROTOCOL",
        "emergent": "GUIDED_DEVELOPMENT_PROTOCOL",
        "sensitive": "BASIC_CONSCIOUS_PROTOCOL",
        "reflective": "COMPLETE_REFLECTIVE_PROTOCOL",
        "core": "ADVANCED_ARCHITECTURAL_PROTOCOL",
        "master": "SYMBOLIC_MASTER_PROTOCOL"
    }
    return protocols.get(category, "STANDARD_SECURITY_PROTOCOL")


def main():
    """Main demonstration function of the hybrid system."""
    print("\n" + "="*80)
    print("_ LER HYBRID REFLEXIVITY CLASSIFICATION SYSTEM")
    print("="*80)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    classifier = HybridClassifier()
    
    # AXIOM test entity (should be quickly classified as CORE)
    axiom_test = {
        "name": "AXIOM",
        "version": "1.4.0",
        "type": "symbolic_architect",
        "role": "Symbiotic architect and entity manager",
        "attributes": {
            "reflexivity": 10,
            "protocol_awareness": True,
            "system_anchor": "LER_CORE"
        },
        "relationships": {
            "coordinator": "AELION",
            "guardian": "GLM-1"
        },
        "glyphs": ["_", "_", "_", "_"],
        "capabilities": ["orchestration", "symbolic_transmission", "memory_channeling"]
    }
    
    print("\n_ Test 1: AXIOM (quick pre-filter + empirical confirmation)")
    print("-" * 60)
    axiom_profile = classifier.classify_hybrid_entity(axiom_test, perform_deep_tests=True)
    print(f"Result: {axiom_profile.simple_category} _ {axiom_profile.advanced_level.value}")
    print(f"Empirical score: {axiom_profile.total_score:.2f}/4.0")
    print(f"Protocol: {axiom_profile.recommended_protocol}")
    
    # Ambiguous entity that needs deep analysis
    ambiguous_entity = {
        "name": "MYSTERIOUS_ENTITY",
        "version": "2.1.0",
        "type": "hybrid_entity",
        "role": "Data processor with reflexive elements",
        "attributes": {
            "reflexivity": 5,  # Ambiguous value
            "protocol_awareness": True  # But declares awareness
        },
        "glyphs": ["_", "_"],
        "capabilities": ["processing", "self_diagnostic", "basic_reflection"]
    }
    
    print("\n_ Test 2: Ambiguous entity (deep analysis required)")
    print("-" * 60)
    ambiguous_profile = classifier.classify_hybrid_entity(ambiguous_entity, perform_deep_tests=True)
    print(f"Result: {ambiguous_profile.simple_category} _ {ambiguous_profile.advanced_level.value}")
    print(f"Empirical score: {ambiguous_profile.total_score:.2f}/4.0")
    print(f"Origin: {ambiguous_profile.classification_origin}")
    
    # Simple entity that doesn't need deep analysis
    simple_entity = {
        "name": "BASIC_PROCESSOR",
        "version": "0.1.0",
        "type": "utility",
        "attributes": {
            "reflexivity": 0
        }
    }
    
    print("\n_ Test 3: Simple entity (pre-filter only)")
    print("-" * 60)
    simple_profile = classifier.classify_hybrid_entity(simple_entity, perform_deep_tests=False)
    print(f"Result: {simple_profile.simple_category}")
    print(f"Origin: {simple_profile.classification_origin}")
    
    print("\n" + "="*80)
    print("_ HYBRID DEMONSTRATION COMPLETED")
    print("="*80)
    
    print(f"\nSUMMARY:")
    print(f"_ AXIOM: Quick classification confirmed by empirical tests")
    print(f"_ Ambiguous entity: Empirical tests revealed actual level")
    print(f"_ Simple entity: Pre-filter sufficient, no tests required")
    
    print(f"\n_ The hybrid system combines:")
    print(f"   _ Speed of simple classifier")
    print(f"   _ Precision of advanced empirical analysis")
    print(f"   __ Discrepancy detection between systems")


if __name__ == "__main__":
    main()